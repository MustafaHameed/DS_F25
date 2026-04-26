from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

os.environ.setdefault("OMP_NUM_THREADS", "1")

from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score


RSEED = 2026
ROLE_STATES = ["Isolate", "Mediator", "Leader"]
GPA_LEVELS = ["Low", "Middle", "High"]
ROLE_COLUMNS = [f"Role_{index}" for index in range(1, 21)]
CLUSTER_COUNT = 3


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


def compute_transition_counts(sequence_frame: pd.DataFrame) -> pd.DataFrame:
    counts = pd.DataFrame(0, index=ROLE_STATES, columns=ROLE_STATES, dtype=float)
    for _, row in sequence_frame[ROLE_COLUMNS].iterrows():
        sequence = row.tolist()
        for previous_role, next_role in zip(sequence[:-1], sequence[1:]):
            counts.loc[previous_role, next_role] += 1
    return counts


def normalize_transition_counts(counts: pd.DataFrame) -> pd.DataFrame:
    row_totals = counts.sum(axis=1).replace(0, np.nan)
    return counts.div(row_totals, axis=0).fillna(0.0)


def build_sequence_features(sequence_frame: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, float | int | str]] = []
    for _, row in sequence_frame.iterrows():
        sequence = row[ROLE_COLUMNS].tolist()
        role_counts = pd.Series(sequence).value_counts(normalize=True)
        transition_counts = compute_transition_counts(pd.DataFrame([row]))
        transition_rates = normalize_transition_counts(transition_counts)

        feature_row: dict[str, float | int | str] = {
            "ID": int(row["ID"]),
            "GPA": row["GPA"],
            "initial_role": sequence[0],
            "final_role": sequence[-1],
        }
        for state in ROLE_STATES:
            feature_row[f"share_{state.lower()}"] = float(role_counts.get(state, 0.0))
            feature_row[f"starts_{state.lower()}"] = float(sequence[0] == state)
            feature_row[f"ends_{state.lower()}"] = float(sequence[-1] == state)
        for source in ROLE_STATES:
            for target in ROLE_STATES:
                feature_row[f"trans_{source.lower()}_{target.lower()}"] = float(transition_rates.loc[source, target])
        rows.append(feature_row)

    return pd.DataFrame(rows)


def evaluate_cluster_range(features: pd.DataFrame) -> pd.DataFrame:
    feature_columns = [column for column in features.columns if column not in {"ID", "GPA", "initial_role", "final_role"}]
    matrix = features[feature_columns]
    rows: list[dict[str, float | int]] = []
    for cluster_count in range(2, 6):
        model = GaussianMixture(
            n_components=cluster_count,
            covariance_type="diag",
            random_state=RSEED,
            n_init=20,
        )
        model.fit(matrix)
        labels = model.predict(matrix)
        rows.append(
            {
                "clusters": cluster_count,
                "bic": round(float(model.bic(matrix)), 2),
                "silhouette": round(float(silhouette_score(matrix, labels)), 4),
            }
        )
    return pd.DataFrame(rows)


def assign_cluster_names(feature_frame: pd.DataFrame) -> dict[int, str]:
    cluster_summary = (
        feature_frame.groupby("cluster_raw", as_index=False)[["share_isolate", "share_mediator", "share_leader"]]
        .mean()
    )
    leader_cluster = int(cluster_summary.sort_values("share_leader", ascending=False).iloc[0]["cluster_raw"])
    remaining = cluster_summary[cluster_summary["cluster_raw"] != leader_cluster]
    isolate_cluster = int(remaining.sort_values("share_isolate", ascending=False).iloc[0]["cluster_raw"])
    mediator_cluster = int(
        cluster_summary[~cluster_summary["cluster_raw"].isin([leader_cluster, isolate_cluster])].iloc[0]["cluster_raw"]
    )
    return {
        leader_cluster: "Mainly leader",
        isolate_cluster: "Isolate/mediator",
        mediator_cluster: "Mediator/leader",
    }


def fit_cluster_model(features: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    feature_columns = [column for column in features.columns if column not in {"ID", "GPA", "initial_role", "final_role"}]
    matrix = features[feature_columns]
    model = GaussianMixture(
        n_components=CLUSTER_COUNT,
        covariance_type="diag",
        random_state=RSEED,
        n_init=30,
    )
    model.fit(matrix)

    assigned = features.copy()
    assigned["cluster_raw"] = model.predict(matrix)
    assigned["cluster_label"] = assigned["cluster_raw"].map(assign_cluster_names(assigned))

    profiles: list[dict[str, object]] = []
    for cluster_label, cluster_frame in assigned.groupby("cluster_label"):
        member_ids = cluster_frame["ID"].tolist()
        sequences = full_sequences[full_sequences["ID"].isin(member_ids)]
        transitions = normalize_transition_counts(compute_transition_counts(sequences))
        prototype_sequence = []
        for column in ROLE_COLUMNS:
            prototype_sequence.append(sequences[column].mode().iat[0])
        gpa_distribution = cluster_frame["GPA"].value_counts(normalize=True).reindex(GPA_LEVELS, fill_value=0.0)
        dominant_roles = (
            cluster_frame[["share_isolate", "share_mediator", "share_leader"]]
            .mean()
            .rename(index={
                "share_isolate": "Isolate",
                "share_mediator": "Mediator",
                "share_leader": "Leader",
            })
            .sort_values(ascending=False)
        )

        profiles.append(
            {
                "cluster_label": cluster_label,
                "size": int(len(cluster_frame)),
                "prototype_sequence": prototype_sequence,
                "dominant_roles": dominant_roles.index.tolist(),
                "gpa_distribution": {key: round(float(value), 3) for key, value in gpa_distribution.items()},
                "transition_matrix": transitions.round(4).to_dict(),
            }
        )

    return assigned, pd.DataFrame(profiles)


def build_dashboard_payload(
    original_data: pd.DataFrame,
    cluster_selection: pd.DataFrame,
    cluster_metrics: pd.DataFrame,
    cluster_profiles: pd.DataFrame,
    overall_transition: pd.DataFrame,
    gpa_transitions: dict[str, pd.DataFrame],
) -> dict[str, object]:
    cluster_profiles_records = cluster_profiles.to_dict(orient="records")
    samples = original_data.copy()
    samples["sequence_preview"] = samples[ROLE_COLUMNS].apply(lambda row: " -> ".join(row.tolist()), axis=1)
    samples = samples.merge(cluster_selection[["ID", "cluster_label"]], on="ID", how="left")
    samples = samples[["ID", "GPA", "cluster_label", "sequence_preview"]].head(160)

    return {
        "project": {
            "title": "Role Transition Markov Studio",
            "generated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "backend": "Python",
            "source_chapter": "Chapter 12",
            "source_qmd": "ch12-markov.qmd",
            "source_notebook": "ch12-markov.ipynb",
        },
        "overview": {
            "total_learners": int(len(original_data)),
            "sequence_length": len(ROLE_COLUMNS),
            "role_states": len(ROLE_STATES),
            "chosen_clusters": CLUSTER_COUNT,
        },
        "role_states": ROLE_STATES,
        "cluster_metrics": json.loads(cluster_metrics.to_json(orient="records")),
        "overall_transition": overall_transition.round(4).to_dict(orient="index"),
        "gpa_transitions": {gpa: matrix.round(4).to_dict(orient="index") for gpa, matrix in gpa_transitions.items()},
        "cluster_profiles": cluster_profiles_records,
        "manual_demo": {
            "allowed_roles": ROLE_STATES,
            "default_sequence": original_data.iloc[0][ROLE_COLUMNS].tolist(),
            "cluster_models": {
                row["cluster_label"]: {
                    "prototype_sequence": row["prototype_sequence"],
                    "transition_matrix": row["transition_matrix"],
                    "gpa_distribution": row["gpa_distribution"],
                    "dominant_roles": row["dominant_roles"],
                }
                for row in cluster_profiles_records
            },
        },
        "samples": json.loads(samples.to_json(orient="records")),
    }


def run_pipeline() -> dict[str, object]:
    global full_sequences

    paths = project_paths()
    data_path = paths["data_raw_dir"] / "simulated_roles.csv"
    if not data_path.exists():
        raise FileNotFoundError("Expected simulated_roles.csv inside data/raw before running the backend.")

    original_data = pd.read_csv(data_path)
    full_sequences = original_data.copy()

    overall_transition = normalize_transition_counts(compute_transition_counts(original_data))
    gpa_transitions = {
        gpa: normalize_transition_counts(compute_transition_counts(frame))
        for gpa, frame in original_data.groupby("GPA")
    }

    feature_frame = build_sequence_features(original_data)
    cluster_metrics = evaluate_cluster_range(feature_frame)
    cluster_selection, cluster_profiles = fit_cluster_model(feature_frame)

    feature_frame.merge(cluster_selection[["ID", "cluster_label"]], on="ID", how="left").to_csv(
        paths["data_processed_dir"] / "sequence_features.csv", index=False
    )
    cluster_selection.to_csv(paths["output_dir"] / "cluster_assignments.csv", index=False)
    cluster_metrics.to_csv(paths["output_dir"] / "cluster_metrics.csv", index=False)
    cluster_profiles.to_csv(paths["output_dir"] / "cluster_profiles.csv", index=False)
    overall_transition.to_csv(paths["output_dir"] / "overall_transition_matrix.csv")
    for gpa, matrix in gpa_transitions.items():
        matrix.to_csv(paths["output_dir"] / f"transition_matrix_{gpa.lower()}.csv")

    payload = build_dashboard_payload(
        original_data,
        cluster_selection,
        cluster_metrics,
        cluster_profiles,
        overall_transition,
        gpa_transitions,
    )
    (paths["output_dir"] / "dashboard.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


if __name__ == "__main__":
    payload = run_pipeline()
    print(json.dumps(payload["overview"], indent=2))