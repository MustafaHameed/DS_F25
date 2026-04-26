from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import OneHotEncoder


ENGAGEMENT_STATES = ["Active", "Average", "Disengaged"]
ACHIEVEMENT_STATES = ["Achiever", "Intermediate", "Low"]
STEP_COUNT = 8
CLUSTER_COUNT = 6


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


def build_channel_distribution(dataframe: pd.DataFrame, column_name: str, states: list[str]) -> pd.DataFrame:
    counts = (
        dataframe.groupby(["Sequence", column_name], as_index=False)
        .size()
        .rename(columns={"size": "count"})
    )
    totals = counts.groupby("Sequence")["count"].transform("sum")
    counts["proportion"] = counts["count"] / totals
    counts[column_name] = pd.Categorical(counts[column_name], categories=states, ordered=True)
    return counts.sort_values(["Sequence", column_name])


def build_user_sequences(dataframe: pd.DataFrame) -> pd.DataFrame:
    sequence_frame = dataframe.sort_values(["UserID", "Sequence"]).copy()
    sequence_frame["combined_state"] = sequence_frame["Engagement"] + " | " + sequence_frame["Achievement"]
    engagement_pivot = sequence_frame.pivot(index="UserID", columns="Sequence", values="Engagement")
    achievement_pivot = sequence_frame.pivot(index="UserID", columns="Sequence", values="Achievement")
    combined_pivot = sequence_frame.pivot(index="UserID", columns="Sequence", values="combined_state")

    users = engagement_pivot.index.to_series().rename("UserID")
    combined = pd.DataFrame(users).reset_index(drop=True)
    for step in range(1, STEP_COUNT + 1):
        combined[f"engagement_{step}"] = engagement_pivot[step].values
        combined[f"achievement_{step}"] = achievement_pivot[step].values
        combined[f"combined_{step}"] = combined_pivot[step].values
    return combined


def evaluate_cluster_range(sequence_table: pd.DataFrame) -> tuple[pd.DataFrame, OneHotEncoder, list[str], pd.DataFrame]:
    combined_columns = [column for column in sequence_table.columns if column.startswith("combined_")]
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    encoded = encoder.fit_transform(sequence_table[combined_columns])

    rows: list[dict[str, float | int]] = []
    for cluster_count in range(2, 7):
        labels = AgglomerativeClustering(n_clusters=cluster_count, linkage="ward").fit_predict(encoded)
        rows.append(
            {
                "clusters": cluster_count,
                "silhouette": round(float(silhouette_score(encoded, labels)), 4),
            }
        )
    return pd.DataFrame(rows), encoder, combined_columns, pd.DataFrame(encoded)


def build_cluster_profiles(sequence_table: pd.DataFrame, raw_labels: pd.Series, grade_lookup: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    working = sequence_table.copy()
    working["cluster_raw"] = raw_labels
    working = working.merge(grade_lookup, on="UserID", how="left")

    engagement_scores = {"Disengaged": 1, "Average": 2, "Active": 3}
    achievement_scores = {"Low": 1, "Intermediate": 2, "Achiever": 3}

    raw_profiles: list[dict[str, object]] = []
    for raw_cluster, cluster_frame in working.groupby("cluster_raw"):
        prototype_engagement = []
        prototype_achievement = []
        combined_counts: dict[str, int] = {}
        engagement_score_values: list[int] = []
        achievement_score_values: list[int] = []

        for step in range(1, STEP_COUNT + 1):
            engagement_mode = cluster_frame[f"engagement_{step}"].mode().iat[0]
            achievement_mode = cluster_frame[f"achievement_{step}"].mode().iat[0]
            prototype_engagement.append(engagement_mode)
            prototype_achievement.append(achievement_mode)

            engagement_score_values.extend(cluster_frame[f"engagement_{step}"].map(engagement_scores).tolist())
            achievement_score_values.extend(cluster_frame[f"achievement_{step}"].map(achievement_scores).tolist())

            for combined_state, count in cluster_frame[f"combined_{step}"].value_counts().items():
                combined_counts[combined_state] = combined_counts.get(combined_state, 0) + int(count)

        raw_profiles.append(
            {
                "cluster_raw": int(raw_cluster),
                "size": int(len(cluster_frame)),
                "mean_final_grade": round(float(cluster_frame["Final_Grade"].mean()), 2),
                "mean_engagement_score": round(sum(engagement_score_values) / len(engagement_score_values), 3),
                "mean_achievement_score": round(sum(achievement_score_values) / len(achievement_score_values), 3),
                "prototype_engagement": prototype_engagement,
                "prototype_achievement": prototype_achievement,
                "dominant_combined_states": [
                    state for state, _ in sorted(combined_counts.items(), key=lambda item: item[1], reverse=True)[:3]
                ],
            }
        )

    profiles = pd.DataFrame(raw_profiles).sort_values(
        ["mean_engagement_score", "mean_achievement_score", "mean_final_grade"], ascending=False
    ).reset_index(drop=True)
    profiles["cluster_id"] = range(1, len(profiles) + 1)
    profiles["cluster_label"] = profiles["cluster_id"].apply(lambda value: f"Cluster {value}")
    mapping = dict(zip(profiles["cluster_raw"], profiles["cluster_label"]))

    assignments = working.copy()
    assignments["cluster_label"] = assignments["cluster_raw"].map(mapping)
    return profiles, assignments


def build_dashboard_payload(
    original_data: pd.DataFrame,
    engagement_distribution: pd.DataFrame,
    achievement_distribution: pd.DataFrame,
    cluster_validation: pd.DataFrame,
    cluster_profiles: pd.DataFrame,
    assignments: pd.DataFrame,
) -> dict[str, object]:
    cluster_profile_records = cluster_profiles.to_dict(orient="records")
    sample_columns = [column for column in assignments.columns if column.startswith("combined_")]
    samples = assignments.copy()
    samples["multichannel_path"] = samples[sample_columns].apply(lambda row: " -> ".join(row.tolist()), axis=1)
    samples = samples[["UserID", "cluster_label", "Final_Grade", "multichannel_path"]].head(180)

    default_profile = cluster_profile_records[0]

    return {
        "project": {
            "title": "Multichannel Learning Trajectory Studio",
            "generated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "backend": "Python",
            "source_chapter": "Chapter 13",
            "source_qmd": "ch13-multi.qmd",
            "source_notebook": "ch13-multichannel.ipynb",
        },
        "overview": {
            "total_records": int(len(original_data)),
            "unique_students": int(original_data["UserID"].nunique()),
            "sequence_length": STEP_COUNT,
            "chosen_clusters": CLUSTER_COUNT,
        },
        "engagement_states": ENGAGEMENT_STATES,
        "achievement_states": ACHIEVEMENT_STATES,
        "engagement_distribution": json.loads(engagement_distribution.to_json(orient="records")),
        "achievement_distribution": json.loads(achievement_distribution.to_json(orient="records")),
        "cluster_validation": json.loads(cluster_validation.to_json(orient="records")),
        "cluster_profiles": cluster_profile_records,
        "manual_demo": {
            "field_schema": [
                {
                    "step": step,
                    "default_engagement": default_profile["prototype_engagement"][step - 1],
                    "default_achievement": default_profile["prototype_achievement"][step - 1],
                }
                for step in range(1, STEP_COUNT + 1)
            ],
            "profiles": {
                row["cluster_label"]: {
                    "prototype_engagement": row["prototype_engagement"],
                    "prototype_achievement": row["prototype_achievement"],
                    "dominant_combined_states": row["dominant_combined_states"],
                    "mean_final_grade": row["mean_final_grade"],
                }
                for row in cluster_profile_records
            },
        },
        "samples": json.loads(samples.to_json(orient="records")),
    }


def run_pipeline() -> dict[str, object]:
    paths = project_paths()
    data_path = paths["data_raw_dir"] / "SequenceEngagementAchievement.xlsx"
    if not data_path.exists():
        raise FileNotFoundError("Expected SequenceEngagementAchievement.xlsx inside data/raw before running the backend.")

    original_data = pd.read_excel(data_path).sort_values(["UserID", "Sequence"])
    engagement_distribution = build_channel_distribution(original_data, "Engagement", ENGAGEMENT_STATES)
    achievement_distribution = build_channel_distribution(original_data, "Achievement", ACHIEVEMENT_STATES)
    user_sequences = build_user_sequences(original_data)
    grade_lookup = original_data.groupby("UserID", as_index=False)["Final_Grade"].mean()

    cluster_validation, _, _, encoded = evaluate_cluster_range(user_sequences)
    raw_labels = AgglomerativeClustering(n_clusters=CLUSTER_COUNT, linkage="ward").fit_predict(encoded)
    cluster_profiles, assignments = build_cluster_profiles(user_sequences, pd.Series(raw_labels), grade_lookup)

    user_sequences.to_csv(paths["data_processed_dir"] / "user_multichannel_sequences.csv", index=False)
    engagement_distribution.to_csv(paths["output_dir"] / "engagement_distribution.csv", index=False)
    achievement_distribution.to_csv(paths["output_dir"] / "achievement_distribution.csv", index=False)
    cluster_validation.to_csv(paths["output_dir"] / "cluster_validation.csv", index=False)
    cluster_profiles.to_csv(paths["output_dir"] / "cluster_profiles.csv", index=False)
    assignments.to_csv(paths["output_dir"] / "cluster_assignments.csv", index=False)

    payload = build_dashboard_payload(
        original_data,
        engagement_distribution,
        achievement_distribution,
        cluster_validation,
        cluster_profiles,
        assignments,
    )
    (paths["output_dir"] / "dashboard.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


if __name__ == "__main__":
    payload = run_pipeline()
    print(json.dumps(payload["overview"], indent=2))