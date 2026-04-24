from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
from pathlib import Path


def ensure_dependencies() -> None:
    required = {
        "pandas": "pandas",
        "numpy": "numpy",
        "sklearn": "scikit-learn",
        "joblib": "joblib",
    }

    for module_name, package_name in required.items():
        try:
            importlib.import_module(module_name)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


ensure_dependencies()

os.environ.setdefault("OMP_NUM_THREADS", "3")

import joblib
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler


RSEED = 2024
FEATURE_MAP = {
    "PRE_ENG_COND": "BehvEngmnt",
    "PRE_ENG_COGN": "CognEngmnt",
    "PRE_ENG_EMOC": "EmotEngmnt",
}
PROFILE_COUNT = 3


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


def round_numeric_columns(dataframe: pd.DataFrame, digits: int = 4) -> pd.DataFrame:
    result = dataframe.copy()
    numeric_columns = result.select_dtypes(include=[np.number]).columns
    result.loc[:, numeric_columns] = result.loc[:, numeric_columns].round(digits)
    return result


def load_source_data(paths: dict[str, Path]) -> pd.DataFrame:
    source_path = paths["data_raw_dir"] / "Manuscript_School Engagment.csv"
    if not source_path.exists():
        raise FileNotFoundError("Manuscript_School Engagment.csv was not found in data/raw.")

    dataset = pd.read_csv(source_path, sep=";", decimal=",", encoding="latin1", low_memory=False)
    dataset.columns = [str(column).replace("ï»¿", "").replace("\ufeff", "").strip() for column in dataset.columns]
    return dataset


def describe_profile(profile_row: pd.Series, global_means: pd.Series) -> tuple[list[str], list[str]]:
    deltas = (profile_row - global_means).sort_values(ascending=False)
    high = deltas.head(2).index.tolist()
    low = deltas.tail(1).index.tolist()
    return high, low


def fit_candidate_models(scaled_values: np.ndarray) -> tuple[pd.DataFrame, dict[int, GaussianMixture]]:
    rows = []
    models: dict[int, GaussianMixture] = {}

    for components in range(2, 7):
        model = GaussianMixture(
            n_components=components,
            covariance_type="diag",
            init_params="random_from_data",
            n_init=20,
            random_state=RSEED,
        )
        model.fit(scaled_values)
        models[components] = model
        rows.append(
            {
                "components": components,
                "bic": model.bic(scaled_values),
                "aic": model.aic(scaled_values),
            }
        )

    return pd.DataFrame(rows), models


def build_dashboard_payload(
    clean_data: pd.DataFrame,
    feature_columns: list[str],
    profile_assignments: pd.DataFrame,
    profile_means: pd.DataFrame,
    model_selection: pd.DataFrame,
    gmm: GaussianMixture,
    scaler: StandardScaler,
) -> dict[str, object]:
    profile_sizes = profile_assignments.groupby("profile", as_index=False).size().rename(columns={"size": "count"})
    global_means = profile_assignments[feature_columns].mean()
    posterior_columns = [f"ProbProfile{profile_number}" for profile_number in range(1, PROFILE_COUNT + 1)]

    profile_cards = []
    for _, row in profile_means.iterrows():
        profile_id = int(row["profile"])
        high, low = describe_profile(row[feature_columns], global_means)
        subset = profile_assignments.loc[profile_assignments["profile"] == profile_id]
        profile_cards.append(
            {
                "profile": profile_id,
                "label": f"Profile {profile_id}",
                "size": int(profile_sizes.loc[profile_sizes["profile"] == profile_id, "count"].iloc[0]),
                "mix_weight": float(gmm.weights_[profile_id - 1]),
                "top_high": high,
                "top_low": low,
                "means": {column: float(row[column]) for column in feature_columns},
                "avg_assignment_probability": float(subset["AssignmentProbability"].mean()),
            }
        )

    defaults = profile_assignments[feature_columns].median()
    overview = {
        "total_students": int(len(clean_data)),
        "feature_count": len(feature_columns),
        "chosen_profiles": PROFILE_COUNT,
        "avg_assignment_probability": float(profile_assignments["AssignmentProbability"].mean()),
        "avg_entropy": float(profile_assignments["Entropy"].mean()),
    }

    payload = {
        "project": {
            "title": "Student Engagement Profile Studio",
            "generated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "backend": "Python",
            "source_chapter": "Chapter 09",
            "source_qmd": "ch09-model.qmd",
            "source_notebook": "ch09-model-based-clustering.ipynb",
        },
        "overview": overview,
        "feature_columns": feature_columns,
        "field_schema": [
            {
                "name": column,
                "label": column,
                "default": float(defaults[column]),
                "min": float(profile_assignments[column].min()),
                "max": float(profile_assignments[column].max()),
                "step": 0.01,
            }
            for column in feature_columns
        ],
        "scaler": {
            "feature_order": feature_columns,
            "mean": scaler.mean_.tolist(),
            "scale": scaler.scale_.tolist(),
        },
        "gmm": {
            "weights": gmm.weights_.tolist(),
            "means": gmm.means_.tolist(),
            "variances": gmm.covariances_.tolist(),
        },
        "model_selection": json.loads(round_numeric_columns(model_selection).to_json(orient="records")),
        "profile_sizes": json.loads(profile_sizes.to_json(orient="records")),
        "profile_means": json.loads(round_numeric_columns(profile_means).to_json(orient="records")),
        "profiles": profile_cards,
        "members": json.loads(round_numeric_columns(profile_assignments[["student_id", "profile", *feature_columns, "AssignmentProbability", "Entropy", *posterior_columns]]).to_json(orient="records")),
    }

    return payload


def run_pipeline() -> dict[str, object]:
    paths = project_paths()
    source_data = load_source_data(paths)
    required_columns = ["alumno.pret", *FEATURE_MAP.keys()]
    missing = [column for column in required_columns if column not in source_data.columns]
    if missing:
        raise ValueError(f"Missing required Chapter 09 columns: {missing}")

    clean_data = source_data.loc[:, required_columns].copy()
    clean_data = clean_data.rename(columns={"alumno.pret": "student_id", **FEATURE_MAP}).dropna().copy()
    clean_data.to_csv(paths["data_processed_dir"] / "engagement_profiles_clean.csv", index=False)

    feature_columns = list(FEATURE_MAP.values())
    scaler = StandardScaler()
    scaled_values = scaler.fit_transform(clean_data[feature_columns])
    pd.DataFrame(scaled_values, columns=feature_columns).to_csv(paths["data_processed_dir"] / "engagement_profiles_scaled.csv", index=False)

    model_selection, candidate_models = fit_candidate_models(scaled_values)
    model = candidate_models[PROFILE_COUNT]
    labels = model.predict(scaled_values) + 1
    posterior = model.predict_proba(scaled_values)
    assignment_probability = posterior.max(axis=1)
    entropy = -np.sum(posterior * np.log(posterior + 1e-12), axis=1)

    posterior_columns = [f"ProbProfile{profile_number}" for profile_number in range(1, PROFILE_COUNT + 1)]
    assignments = clean_data.copy()
    assignments["profile"] = labels.astype(int)
    assignments["AssignmentProbability"] = assignment_probability
    assignments["Entropy"] = entropy

    for index, column_name in enumerate(posterior_columns):
        assignments[column_name] = posterior[:, index]

    profile_means = assignments.groupby("profile", as_index=False)[feature_columns].mean()

    assignments_out = round_numeric_columns(assignments)
    profile_means_out = round_numeric_columns(profile_means)
    model_selection_out = round_numeric_columns(model_selection)

    assignments_out.to_csv(paths["output_dir"] / "profile_assignments.csv", index=False)
    profile_means_out.to_csv(paths["output_dir"] / "profile_means.csv", index=False)
    model_selection_out.to_csv(paths["output_dir"] / "model_selection.csv", index=False)

    joblib.dump(scaler, paths["models_dir"] / "scaler.joblib")
    joblib.dump(model, paths["models_dir"] / "gmm.joblib")

    payload = build_dashboard_payload(
        clean_data=clean_data,
        feature_columns=feature_columns,
        profile_assignments=assignments_out,
        profile_means=profile_means_out,
        model_selection=model_selection_out,
        gmm=model,
        scaler=scaler,
    )
    (paths["output_dir"] / "dashboard.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


if __name__ == "__main__":
    result = run_pipeline()
    print(json.dumps(result["overview"], indent=2))