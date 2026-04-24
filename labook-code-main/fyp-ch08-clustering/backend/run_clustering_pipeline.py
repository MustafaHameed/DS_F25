from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path


def ensure_dependencies() -> None:
    required = {
        "pandas": "pandas",
        "numpy": "numpy",
        "sklearn": "scikit-learn",
        "scipy": "scipy",
        "joblib": "joblib",
    }

    for module_name, package_name in required.items():
        try:
            importlib.import_module(module_name)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


ensure_dependencies()

import joblib
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist
from sklearn.metrics import davies_bouldin_score, silhouette_score
from sklearn.preprocessing import StandardScaler


RSEED = 2024


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


def pretty_name(column_name: str) -> str:
    return column_name.replace("_", " ").replace(".", " ").title()


def round_numeric_columns(dataframe: pd.DataFrame, digits: int = 4) -> pd.DataFrame:
    result = dataframe.copy()
    numeric_columns = result.select_dtypes(include=[np.number]).columns
    result.loc[:, numeric_columns] = result.loc[:, numeric_columns].round(digits)
    return result


def load_source_data(paths: dict[str, Path]) -> tuple[pd.DataFrame, str]:
    centralities_path = paths["data_raw_dir"] / "Centralities.csv"
    if not centralities_path.exists():
        raise FileNotFoundError("Centralities.csv was not found in data/raw.")

    dataset = pd.read_csv(centralities_path)
    identifier_column = "name" if "name" in dataset.columns else dataset.columns[0]
    return dataset, identifier_column


def describe_cluster(cluster_profile: pd.Series, global_means: pd.Series) -> tuple[list[str], list[str]]:
    deltas = (cluster_profile - global_means).sort_values(ascending=False)
    top_high = [pretty_name(column) for column in deltas.head(3).index]
    top_low = [pretty_name(column) for column in deltas.tail(2).index]
    return top_high, top_low


def build_dashboard_payload(
    dataset: pd.DataFrame,
    clustered: pd.DataFrame,
    feature_columns: list[str],
    scaler: StandardScaler,
    validation_metrics: pd.DataFrame,
    chosen_k: int,
    cluster_profiles: pd.DataFrame,
    centroids_scaled: pd.DataFrame,
) -> dict[str, object]:
    cluster_sizes = clustered.groupby("cluster", as_index=False).size().rename(columns={"size": "count"})
    global_means = clustered[feature_columns].mean()

    cluster_cards = []
    for _, row in cluster_profiles.iterrows():
        cluster_id = int(row["cluster"])
        profile = row[feature_columns]
        top_high, top_low = describe_cluster(profile, global_means)
        centroid_scaled = centroids_scaled.loc[centroids_scaled["cluster"] == cluster_id, feature_columns].iloc[0]
        cluster_cards.append(
            {
                "cluster": cluster_id,
                "label": f"Cluster {cluster_id}",
                "size": int(cluster_sizes.loc[cluster_sizes["cluster"] == cluster_id, "count"].iloc[0]),
                "top_high": top_high,
                "top_low": top_low,
                "centroid_original": {column: float(profile[column]) for column in feature_columns},
                "centroid_scaled": {column: float(centroid_scaled[column]) for column in feature_columns},
            }
        )

    chosen_validation = validation_metrics.loc[validation_metrics["k"] == chosen_k].iloc[0]
    default_values = clustered[feature_columns].median()

    payload = {
        "project": {
            "title": "Student Network Clustering Studio",
            "generated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "backend": "Python",
            "source_chapter": "Chapter 08",
            "source_qmd": "ch08-clustering.qmd",
            "source_notebook": "ch08-clustering.ipynb",
        },
        "overview": {
            "total_nodes": int(len(clustered)),
            "feature_count": int(len(feature_columns)),
            "chosen_clusters": int(chosen_k),
            "best_silhouette": float(chosen_validation["silhouette"]),
        },
        "feature_columns": feature_columns,
        "field_schema": [
            {
                "name": column,
                "label": pretty_name(column),
                "default": float(default_values[column]),
                "min": float(clustered[column].min()),
                "max": float(clustered[column].max()),
                "step": 0.01,
            }
            for column in feature_columns
        ],
        "scaler": {
            "feature_order": feature_columns,
            "mean": scaler.mean_.tolist(),
            "scale": scaler.scale_.tolist(),
        },
        "validation_metrics": json.loads(round_numeric_columns(validation_metrics).to_json(orient="records")),
        "cluster_sizes": json.loads(cluster_sizes.to_json(orient="records")),
        "cluster_profiles": json.loads(round_numeric_columns(cluster_profiles).to_json(orient="records")),
        "clusters": cluster_cards,
        "members": json.loads(clustered[["student_id", "cluster", *feature_columns]].to_json(orient="records")),
    }

    return payload


def run_pipeline() -> dict[str, object]:
    paths = project_paths()
    dataset, identifier_column = load_source_data(paths)

    feature_columns = [
        column
        for column in dataset.select_dtypes(include=[np.number]).columns.tolist()
        if column != identifier_column
    ]
    if not feature_columns:
        raise ValueError("No numeric columns were found in Centralities.csv for clustering.")

    clean_dataset = dataset[[identifier_column, *feature_columns]].dropna().copy()
    clean_dataset = clean_dataset.rename(columns={identifier_column: "student_id"})
    clean_dataset.to_csv(paths["data_processed_dir"] / "clean_centralities.csv", index=False)

    scaler = StandardScaler()
    scaled_values = scaler.fit_transform(clean_dataset[feature_columns])
    scaled_frame = pd.DataFrame(scaled_values, columns=feature_columns)
    scaled_frame.to_csv(paths["data_processed_dir"] / "scaled_centralities.csv", index=False)
    joblib.dump(scaler, paths["models_dir"] / "scaler.joblib")

    distance_vector = pdist(scaled_values, metric="euclidean")
    ward_linkage = linkage(distance_vector, method="ward")

    max_k = min(8, len(clean_dataset) - 1)
    validation_rows = []
    candidate_labels: dict[int, np.ndarray] = {}
    for k in range(2, max_k + 1):
        labels = fcluster(ward_linkage, k, criterion="maxclust")
        candidate_labels[k] = labels
        validation_rows.append(
            {
                "k": k,
                "silhouette": silhouette_score(scaled_values, labels),
                "davies_bouldin": davies_bouldin_score(scaled_values, labels),
            }
        )

    validation_metrics = pd.DataFrame(validation_rows)
    chosen_k = int(validation_metrics.sort_values(["silhouette", "davies_bouldin"], ascending=[False, True]).iloc[0]["k"])
    final_labels = candidate_labels[chosen_k]

    clustered = clean_dataset.copy()
    clustered["cluster"] = final_labels.astype(int)
    cluster_profiles = clustered.groupby("cluster", as_index=False)[feature_columns].mean()
    centroids_scaled = pd.DataFrame(scaled_values, columns=feature_columns).assign(cluster=final_labels).groupby("cluster", as_index=False)[feature_columns].mean()

    cluster_profiles_out = round_numeric_columns(cluster_profiles)
    validation_metrics_out = round_numeric_columns(validation_metrics)
    cluster_assignments_out = round_numeric_columns(clustered)

    cluster_assignments_out.to_csv(paths["output_dir"] / "cluster_assignments.csv", index=False)
    cluster_profiles_out.to_csv(paths["output_dir"] / "cluster_profiles.csv", index=False)
    validation_metrics_out.to_csv(paths["output_dir"] / "validation_metrics.csv", index=False)

    payload = build_dashboard_payload(
        dataset=dataset,
        clustered=cluster_assignments_out,
        feature_columns=feature_columns,
        scaler=scaler,
        validation_metrics=validation_metrics_out,
        chosen_k=chosen_k,
        cluster_profiles=cluster_profiles_out,
        centroids_scaled=round_numeric_columns(centroids_scaled),
    )

    (paths["output_dir"] / "dashboard.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


if __name__ == "__main__":
    result = run_pipeline()
    print(json.dumps(result["overview"], indent=2))