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
        "openpyxl": "openpyxl",
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
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, mean_squared_error, precision_score, r2_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


RSEED = 2023
TOPICAL_ACTIONS = {"General", "Applications", "Theory", "Ethics", "Feedback", "La_types"}


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


def entropy_from_proportions(values: pd.Series | np.ndarray | list[float]) -> float:
    array = np.asarray(values, dtype=float)
    array = array[array > 0]
    if array.size == 0:
        return 0.0

    proportions = array / array.sum()
    return float(-(proportions * np.log2(proportions)).sum())


def rescale_to_100(values: pd.Series) -> pd.Series:
    minimum = values.min()
    maximum = values.max()

    if minimum == maximum:
        return pd.Series(np.full(len(values), 100.0), index=values.index)

    return ((values - minimum) / (maximum - minimum) * 100).round(1)


def round_numeric_columns(dataframe: pd.DataFrame, digits: int = 4) -> pd.DataFrame:
    result = dataframe.copy()
    numeric_columns = result.select_dtypes(include=[np.number]).columns
    result.loc[:, numeric_columns] = result.loc[:, numeric_columns].round(digits)
    return result


def prepare_events(events: pd.DataFrame) -> pd.DataFrame:
    events = events.copy()
    events["timecreated"] = pd.to_datetime(events["timecreated"])
    events = events.sort_values("timecreated").reset_index(drop=True)
    events["wday"] = events["timecreated"].dt.weekday
    events["prev_wday"] = events["wday"].shift(1)
    events["new_week"] = (events["wday"] == 0) & (events["prev_wday"].isna() | (events["prev_wday"] != 0))
    events["course_week"] = events["new_week"].cumsum().astype(int)

    if "Action" in events.columns:
        action_source = events["Action"]
    else:
        action_source = events["action"]

    events["action"] = np.where(
        action_source.isin(TOPICAL_ACTIONS),
        "Materials_" + action_source.astype(str),
        action_source.astype(str),
    )

    processed = events[["user", "timecreated", "course_week", "action"]].rename(
        columns={"timecreated": "ts", "course_week": "week"}
    )

    return processed


def prepare_results(results: pd.DataFrame) -> pd.DataFrame:
    prepared = results[["user", "Final_grade"]].copy()
    median_grade = prepared["Final_grade"].median()
    prepared["Course_outcome"] = np.where(prepared["Final_grade"] > median_grade, "High", "Low")
    return prepared


def sessionize_events(events: pd.DataFrame) -> pd.DataFrame:
    working = events.copy()
    working["ts"] = pd.to_datetime(working["ts"])
    working["date"] = working["ts"].dt.normalize()
    working = working.sort_values(["user", "ts"]).reset_index(drop=True)
    working["ts_diff"] = working.groupby("user")["ts"].diff()
    working["ts_diff_hours"] = working["ts_diff"].dt.total_seconds() / 3600.0
    working["new_session"] = working["ts_diff_hours"].isna() | (working["ts_diff_hours"] >= 1.5)
    working["session_nr"] = working.groupby("user")["new_session"].cumsum().astype(int)
    working["session_id"] = working["user"].astype(str) + "_session_" + working["session_nr"].astype(str)

    session_lengths = working.groupby("session_id").agg(session_start=("ts", "min"), session_end=("ts", "max"))
    session_lengths["session_len"] = (session_lengths["session_end"] - session_lengths["session_start"]).dt.total_seconds()
    working = working.merge(session_lengths[["session_len"]].reset_index(), on="session_id", how="left")

    return working[["user", "ts", "date", "week", "action", "ts_diff", "ts_diff_hours", "session_nr", "session_id", "session_len"]]


def compute_user_features(events_df: pd.DataFrame) -> pd.DataFrame:
    events_df = events_df.copy()

    action_counts = (
        events_df.pivot_table(index="user", columns="action", values="ts", aggfunc="count", fill_value=0)
        .rename(columns=lambda column_name: f"action_cnt_{column_name}")
    )

    daily_counts = events_df.groupby(["user", "date"]).size().reset_index(name="day_cnt")
    avg_actions_per_day = daily_counts.groupby("user")["day_cnt"].median().rename("avg_actions_per_day")
    entropy_daily = daily_counts.groupby("user")["day_cnt"].apply(entropy_from_proportions).rename("entropy_daily_cnts")

    sessions = events_df.groupby(["user", "session_id"], as_index=False).agg(session_len=("session_len", "first"))
    session_cnt = sessions.groupby("user").size().rename("session_cnt")
    median_session_len = sessions.groupby("user")["session_len"].median().rename("median_session_len")
    entropy_session_len = sessions.groupby("user")["session_len"].apply(entropy_from_proportions).rename("entropy_session_len")

    active_days = events_df.groupby("user")["date"].apply(lambda dates: sorted(pd.Series(dates.unique()))).rename("active_days")
    active_days_cnt = active_days.apply(len).rename("active_days_cnt")

    def median_gap_between_days(days: list[pd.Timestamp]) -> float:
        if len(days) <= 1:
            return np.nan
        diffs = np.diff(pd.to_datetime(days)).astype("timedelta64[s]").astype(float) / 86400.0
        return float(np.median(diffs))

    avg_gap_between_active_days = active_days.apply(median_gap_between_days).rename("avg_gap_between_active_days")
    if avg_gap_between_active_days.notna().any():
        replacement_gap = float(avg_gap_between_active_days.max() * 2)
        avg_gap_between_active_days = avg_gap_between_active_days.fillna(replacement_gap)
    else:
        avg_gap_between_active_days = avg_gap_between_active_days.fillna(0.0)

    features = pd.concat(
        [
            action_counts,
            avg_actions_per_day,
            entropy_daily,
            session_cnt,
            median_session_len,
            entropy_session_len,
            active_days_cnt,
            avg_gap_between_active_days,
        ],
        axis=1,
    ).fillna(0.0)

    features.index.name = "user"
    return features.reset_index()


def create_dataset_for_course_success_prediction(events_with_sessions: pd.DataFrame, week_k: int, results_df: pd.DataFrame) -> pd.DataFrame:
    filtered = events_with_sessions[events_with_sessions["week"] <= week_k]
    features = compute_user_features(filtered)
    return features.merge(results_df[["user", "Course_outcome"]], on="user", how="inner")


def create_dataset_for_grade_prediction(events_with_sessions: pd.DataFrame, week_k: int, results_df: pd.DataFrame) -> pd.DataFrame:
    filtered = events_with_sessions[events_with_sessions["week"] <= week_k]
    features = compute_user_features(filtered)
    return features.merge(results_df[["user", "Final_grade"]], on="user", how="inner")


def build_classification_model(dataset: pd.DataFrame) -> tuple[Pipeline, pd.DataFrame]:
    X = dataset.drop(columns=["user", "Course_outcome"])
    y = dataset["Course_outcome"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=RSEED)

    pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("rf", RandomForestClassifier(n_estimators=300, random_state=RSEED)),
        ]
    )
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    metrics = pd.DataFrame(
        [
            {
                "Accuracy": accuracy_score(y_test, y_pred),
                "Precision": precision_score(y_test, y_pred, pos_label="Low", zero_division=0),
                "Recall": recall_score(y_test, y_pred, pos_label="Low", zero_division=0),
                "F1": f1_score(y_test, y_pred, pos_label="Low", zero_division=0),
            }
        ]
    )

    return pipeline, metrics


def build_regression_model(dataset: pd.DataFrame) -> tuple[Pipeline, pd.DataFrame]:
    X = dataset.drop(columns=["user", "Final_grade"])
    y = dataset["Final_grade"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RSEED)

    pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("rf", RandomForestRegressor(n_estimators=300, random_state=RSEED)),
        ]
    )
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    metrics = pd.DataFrame(
        [
            {
                "R2": r2_score(y_test, y_pred),
                "RMSE": mean_squared_error(y_test, y_pred) ** 0.5,
                "MAE": mean_absolute_error(y_test, y_pred),
            }
        ]
    )

    return pipeline, metrics


def extract_feature_importance(model: Pipeline, feature_names: list[str], label: str, top_n: int = 10) -> pd.DataFrame:
    importance = model.named_steps["rf"].feature_importances_
    return (
        pd.DataFrame({"feature": feature_names, "importance": importance, "model": label})
        .sort_values("importance", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def run_pipeline() -> dict[str, object]:
    paths = project_paths()
    events_path = paths["data_raw_dir"] / "Events.xlsx"
    results_path = paths["data_raw_dir"] / "Results.xlsx"

    if not events_path.exists() or not results_path.exists():
        raise FileNotFoundError("Expected local dataset files were not found in data/raw. Copy Events.xlsx and Results.xlsx before running the backend.")

    events = pd.read_excel(events_path, engine="openpyxl")
    results = pd.read_excel(results_path, engine="openpyxl")

    prepared_events = prepare_events(events)
    prepared_results = prepare_results(results)
    events_with_sessions = sessionize_events(prepared_events)

    prepared_events.to_csv(paths["data_processed_dir"] / "events.csv", index=False)
    events_with_sessions.to_csv(paths["data_processed_dir"] / "events_with_sessions.csv", index=False)
    prepared_results.to_csv(paths["data_processed_dir"] / "final_grades.csv", index=False)
    prepared_events.to_pickle(paths["data_processed_dir"] / "events.pkl")
    events_with_sessions.to_pickle(paths["data_processed_dir"] / "events_with_sessions.pkl")
    prepared_results.to_pickle(paths["data_processed_dir"] / "final_grades.pkl")

    classification_models: dict[int, Pipeline] = {}
    classification_rows: list[dict[str, float | int]] = []
    regression_models: dict[int, Pipeline] = {}
    regression_rows: list[dict[str, float | int]] = []

    for week in range(1, 6):
        classification_dataset = create_dataset_for_course_success_prediction(events_with_sessions, week, prepared_results)
        classification_model, classification_metrics = build_classification_model(classification_dataset)
        classification_models[week] = classification_model
        classification_rows.append({"week": week, **classification_metrics.iloc[0].to_dict()})

        regression_dataset = create_dataset_for_grade_prediction(events_with_sessions, week, prepared_results)
        regression_model, regression_metrics = build_regression_model(regression_dataset)
        regression_models[week] = regression_model
        regression_rows.append({"week": week, **regression_metrics.iloc[0].to_dict()})

    classification_metrics = pd.DataFrame(classification_rows)
    regression_metrics = pd.DataFrame(regression_rows)

    best_classification_week = int(classification_metrics.sort_values(["F1", "Accuracy"], ascending=[False, False]).iloc[0]["week"])
    best_regression_week = int(regression_metrics.sort_values(["R2", "RMSE"], ascending=[False, True]).iloc[0]["week"])

    full_classification_dataset = create_dataset_for_course_success_prediction(events_with_sessions, best_classification_week, prepared_results)
    full_regression_dataset = create_dataset_for_grade_prediction(events_with_sessions, best_regression_week, prepared_results)

    full_classification_model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("rf", RandomForestClassifier(n_estimators=300, random_state=RSEED)),
        ]
    )
    full_classification_model.fit(
        full_classification_dataset.drop(columns=["user", "Course_outcome"]),
        full_classification_dataset["Course_outcome"],
    )

    full_regression_model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("rf", RandomForestRegressor(n_estimators=300, random_state=RSEED)),
        ]
    )
    full_regression_model.fit(
        full_regression_dataset.drop(columns=["user", "Final_grade"]),
        full_regression_dataset["Final_grade"],
    )

    classification_features = full_classification_dataset.drop(columns=["user", "Course_outcome"])
    class_probabilities = full_classification_model.predict_proba(classification_features)
    class_labels = list(full_classification_model.classes_)
    low_index = class_labels.index("Low")
    risk_probability = class_probabilities[:, low_index]
    predicted_outcome = np.where(risk_probability >= 0.5, "Low", "High")

    regression_features = full_regression_dataset.drop(columns=["user", "Final_grade"])
    predicted_grade = full_regression_model.predict(regression_features)

    classification_importance = extract_feature_importance(
        full_classification_model,
        classification_features.columns.tolist(),
        "classification",
    )
    regression_importance = extract_feature_importance(
        full_regression_model,
        regression_features.columns.tolist(),
        "regression",
    )

    count_columns = [column for column in classification_features.columns if column.startswith("action_cnt_")]
    activity_summary = full_classification_dataset[["user", *count_columns]].copy()
    if count_columns:
        activity_summary["activity_total"] = activity_summary[count_columns].sum(axis=1)
    else:
        activity_summary["activity_total"] = 0.0
    activity_summary = activity_summary[["user", "activity_total"]]

    last_login = (
        events_with_sessions[events_with_sessions["week"] <= best_classification_week]
        .groupby("user", as_index=False)["ts"]
        .max()
        .rename(columns={"ts": "last_login"})
    )
    last_login["last_login"] = last_login["last_login"].astype(str)

    student_predictions = (
        full_classification_dataset[["user"]]
        .drop_duplicates()
        .merge(last_login, on="user", how="left")
        .merge(
            pd.DataFrame(
                {
                    "user": full_classification_dataset["user"],
                    "risk_probability": risk_probability,
                    "predicted_outcome": predicted_outcome,
                }
            ),
            on="user",
            how="left",
        )
        .merge(
            pd.DataFrame(
                {
                    "user": full_regression_dataset["user"],
                    "predicted_grade": predicted_grade,
                }
            ),
            on="user",
            how="left",
        )
        .merge(activity_summary, on="user", how="left")
    )

    student_predictions["name"] = student_predictions["user"]
    student_predictions["activity_score"] = rescale_to_100(student_predictions["activity_total"].fillna(0.0))
    student_predictions["risk_level"] = np.select(
        [student_predictions["risk_probability"] >= 0.66, student_predictions["risk_probability"] >= 0.33],
        ["high", "medium"],
        default="low",
    )

    student_predictions = student_predictions[
        [
            "user",
            "name",
            "risk_level",
            "risk_probability",
            "predicted_outcome",
            "predicted_grade",
            "activity_score",
            "last_login",
        ]
    ].sort_values("risk_probability", ascending=False)

    risk_counts = (
        student_predictions.groupby("risk_level", as_index=False)
        .size()
        .rename(columns={"size": "count"})
        .sort_values("count", ascending=False)
    )

    classification_metrics_out = round_numeric_columns(classification_metrics)
    regression_metrics_out = round_numeric_columns(regression_metrics)
    classification_importance_out = round_numeric_columns(classification_importance)
    regression_importance_out = round_numeric_columns(regression_importance)
    student_predictions_out = student_predictions.copy()
    student_predictions_out["risk_probability"] = student_predictions_out["risk_probability"].round(4)
    student_predictions_out["predicted_grade"] = student_predictions_out["predicted_grade"].round(2)
    student_predictions_out["activity_score"] = student_predictions_out["activity_score"].round(1)

    classification_metrics_out.to_csv(paths["output_dir"] / "classification_metrics_by_week.csv", index=False)
    regression_metrics_out.to_csv(paths["output_dir"] / "regression_metrics_by_week.csv", index=False)
    classification_importance_out.to_csv(paths["output_dir"] / "feature_importance_classification.csv", index=False)
    regression_importance_out.to_csv(paths["output_dir"] / "feature_importance_regression.csv", index=False)
    student_predictions_out.to_csv(paths["output_dir"] / "student_predictions.csv", index=False)

    joblib.dump(full_classification_model, paths["models_dir"] / "best_classification_model.joblib")
    joblib.dump(full_regression_model, paths["models_dir"] / "best_regression_model.joblib")

    dashboard_payload = {
        "project": {
            "title": "Student Success Prediction Dashboard",
            "generated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "backend": "Python",
            "source_chapter": "Chapter 07",
            "source_qmd": "ch07-prediction.qmd",
            "source_notebook": "ch07-prediction.ipynb",
        },
        "overview": {
            "total_students": int(len(student_predictions_out)),
            "high_risk": int((student_predictions_out["risk_level"] == "high").sum()),
            "medium_risk": int((student_predictions_out["risk_level"] == "medium").sum()),
            "low_risk": int((student_predictions_out["risk_level"] == "low").sum()),
            "best_classification_week": best_classification_week,
            "best_regression_week": best_regression_week,
        },
        "risk_counts": json.loads(risk_counts.to_json(orient="records")),
        "classification_metrics": json.loads(classification_metrics_out.to_json(orient="records")),
        "regression_metrics": json.loads(regression_metrics_out.to_json(orient="records")),
        "top_features": {
            "classification": json.loads(classification_importance_out.to_json(orient="records")),
            "regression": json.loads(regression_importance_out.to_json(orient="records")),
        },
        "students": json.loads(student_predictions_out.to_json(orient="records")),
    }

    (paths["output_dir"] / "dashboard.json").write_text(json.dumps(dashboard_payload, indent=2), encoding="utf-8")
    return dashboard_payload


if __name__ == "__main__":
    payload = run_pipeline()
    print(json.dumps(payload["overview"], indent=2))