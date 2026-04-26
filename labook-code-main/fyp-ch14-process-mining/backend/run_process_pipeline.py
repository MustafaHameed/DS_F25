from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd


SESSION_GAP_SECONDS = 900


def project_paths() -> dict[str, Path]:
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    data_raw_dir = project_root / "data" / "raw"
    data_processed_dir = project_root / "data" / "processed"
    output_dir = project_root / "outputs" / "backend"
    models_dir = output_dir / "models"

    data_processed_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)

    return {
        "project_root": project_root,
        "data_raw_dir": data_raw_dir,
        "data_processed_dir": data_processed_dir,
        "output_dir": output_dir,
        "models_dir": models_dir,
    }


def sessionize_events(events: pd.DataFrame) -> pd.DataFrame:
    sessioned = events.sort_values(["user", "timecreated"]).copy()
    sessioned["time_gap"] = sessioned.groupby("user")["timecreated"].diff().dt.total_seconds()
    sessioned["new_session"] = sessioned["time_gap"].isna() | (sessioned["time_gap"] > SESSION_GAP_SECONDS)
    sessioned["session_nr"] = sessioned.groupby("user")["new_session"].cumsum().astype(int)
    sessioned["session_id"] = sessioned["user"] + "_Session_" + sessioned["session_nr"].astype(str)
    return sessioned


def trim_to_core_activities(events: pd.DataFrame, coverage: float = 0.8) -> tuple[pd.DataFrame, list[str]]:
    activity_counts = events["Action"].value_counts()
    cumulative_share = activity_counts.cumsum() / activity_counts.sum()
    keep_actions = cumulative_share[cumulative_share <= coverage].index.tolist()
    if cumulative_share[cumulative_share > coverage].index.tolist():
        keep_actions.append(cumulative_share[cumulative_share > coverage].index.tolist()[0])
    trimmed = events[events["Action"].isin(keep_actions)].copy()
    return trimmed, keep_actions


def build_activity_frequency(events: pd.DataFrame) -> pd.DataFrame:
    counts = events["Action"].value_counts().rename_axis("Action").reset_index(name="count")
    counts["proportion"] = counts["count"] / counts["count"].sum()
    return counts


def build_activity_frequency_by_group(events: pd.DataFrame) -> pd.DataFrame:
    counts = events.groupby(["AchievingGroup", "Action"], as_index=False).size().rename(columns={"size": "count"})
    counts["proportion"] = counts.groupby("AchievingGroup")["count"].transform(lambda series: series / series.sum())
    return counts.sort_values(["AchievingGroup", "count"], ascending=[True, False])


def build_transitions(events: pd.DataFrame) -> pd.DataFrame:
    ordered = events.sort_values(["session_id", "timecreated"]).copy()
    ordered["next_action"] = ordered.groupby("session_id")["Action"].shift(-1)
    ordered["next_time"] = ordered.groupby("session_id")["timecreated"].shift(-1)
    transitions = ordered.dropna(subset=["next_action"]).copy()
    transitions["gap_seconds"] = (transitions["next_time"] - transitions["timecreated"]).dt.total_seconds()
    return transitions


def summarize_transitions(transitions: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    summary = (
        transitions.groupby(["Action", "next_action"], as_index=False)
        .agg(count=("session_id", "size"), mean_gap_seconds=("gap_seconds", "mean"))
        .sort_values("count", ascending=False)
        .head(top_n)
    )
    summary["mean_gap_seconds"] = summary["mean_gap_seconds"].round(2)
    return summary


def build_markov_model(events: pd.DataFrame, action_catalogue: list[str]) -> dict[str, object]:
    ordered = events.sort_values(["session_id", "timecreated"]).copy()
    session_starts = ordered.groupby("session_id", as_index=False).first()["Action"]
    initial_counts = session_starts.value_counts().reindex(action_catalogue, fill_value=0) + 1
    initial_probs = (initial_counts / initial_counts.sum()).to_dict()

    transition_counts = pd.DataFrame(1.0, index=action_catalogue, columns=action_catalogue)
    for _, frame in ordered.groupby("session_id"):
        actions = frame["Action"].tolist()
        for source, target in zip(actions[:-1], actions[1:]):
            transition_counts.loc[source, target] += 1
    transition_probs = transition_counts.div(transition_counts.sum(axis=1), axis=0)

    return {
        "initial_probs": {key: round(float(value), 6) for key, value in initial_probs.items()},
        "transition_probs": transition_probs.round(6).to_dict(orient="index"),
    }


def build_session_samples(events: pd.DataFrame) -> pd.DataFrame:
    summary = (
        events.sort_values(["session_id", "timecreated"])
        .groupby("session_id", as_index=False)
        .agg(
            user=("user", "first"),
            AchievingGroup=("AchievingGroup", "first"),
            event_count=("Action", "size"),
            action_path=("Action", lambda series: " -> ".join(series.head(12).tolist())),
        )
        .sort_values("event_count", ascending=False)
        .head(180)
    )
    return summary


def build_dashboard_payload(
    original_events: pd.DataFrame,
    trimmed_events: pd.DataFrame,
    activity_frequency: pd.DataFrame,
    activity_frequency_by_group: pd.DataFrame,
    top_transitions: pd.DataFrame,
    group_transitions: dict[str, pd.DataFrame],
    group_models: dict[str, dict[str, object]],
    session_samples: pd.DataFrame,
    action_catalogue: list[str],
) -> dict[str, object]:
    default_path = session_samples.iloc[0]["action_path"].split(" -> ") if not session_samples.empty else action_catalogue[:5]

    return {
        "project": {
            "title": "Learning Process Mining Studio",
            "generated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "backend": "Python",
            "source_chapter": "Chapter 14",
            "source_qmd": "ch14-process.qmd",
            "source_notebook": "ch14-process-mining.ipynb",
        },
        "overview": {
            "total_events": int(len(original_events)),
            "trimmed_events": int(len(trimmed_events)),
            "total_sessions": int(trimmed_events["session_id"].nunique()),
            "distinct_actions": int(len(action_catalogue)),
        },
        "action_catalogue": action_catalogue,
        "activity_frequency": json.loads(activity_frequency.to_json(orient="records")),
        "activity_frequency_by_group": json.loads(activity_frequency_by_group.to_json(orient="records")),
        "top_transitions": json.loads(top_transitions.to_json(orient="records")),
        "group_top_transitions": {group: json.loads(frame.to_json(orient="records")) for group, frame in group_transitions.items()},
        "manual_demo": {
            "default_path": default_path,
            "group_models": group_models,
        },
        "samples": json.loads(session_samples.to_json(orient="records")),
    }


def run_pipeline() -> dict[str, object]:
    paths = project_paths()
    events_path = paths["data_raw_dir"] / "Events.xlsx"
    combined_path = paths["data_raw_dir"] / "AllCombined.xlsx"
    if not events_path.exists() or not combined_path.exists():
        raise FileNotFoundError("Expected Events.xlsx and AllCombined.xlsx inside data/raw before running the backend.")

    events = pd.read_excel(events_path)
    groups = pd.read_excel(combined_path)[["User", "AchievingGroup"]]
    merged = events.merge(groups, left_on="user", right_on="User", how="left").drop(columns=["User"])

    sessioned = sessionize_events(merged)
    trimmed_events, action_catalogue = trim_to_core_activities(sessioned)
    transitions = build_transitions(trimmed_events)

    activity_frequency = build_activity_frequency(trimmed_events)
    activity_frequency_by_group = build_activity_frequency_by_group(trimmed_events)
    top_transitions = summarize_transitions(transitions)
    group_transitions = {
        group: summarize_transitions(frame)
        for group, frame in transitions.groupby("AchievingGroup")
    }
    group_models = {
        group: build_markov_model(frame, action_catalogue)
        for group, frame in trimmed_events.groupby("AchievingGroup")
    }
    session_samples = build_session_samples(trimmed_events)

    sessioned.to_csv(paths["data_processed_dir"] / "sessioned_events.csv", index=False)
    trimmed_events.to_csv(paths["data_processed_dir"] / "trimmed_events.csv", index=False)
    activity_frequency.to_csv(paths["output_dir"] / "activity_frequency.csv", index=False)
    activity_frequency_by_group.to_csv(paths["output_dir"] / "activity_frequency_by_group.csv", index=False)
    top_transitions.to_csv(paths["output_dir"] / "top_transitions.csv", index=False)
    for group, frame in group_transitions.items():
        frame.to_csv(paths["output_dir"] / f"top_transitions_{group.lower().replace(' ', '_')}.csv", index=False)

    payload = build_dashboard_payload(
        merged,
        trimmed_events,
        activity_frequency,
        activity_frequency_by_group,
        top_transitions,
        group_transitions,
        group_models,
        session_samples,
        action_catalogue,
    )
    (paths["output_dir"] / "dashboard.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


if __name__ == "__main__":
    payload = run_pipeline()
    print(json.dumps(payload["overview"], indent=2))