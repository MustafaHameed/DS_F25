bootstrap_packages <- function(packages) {
  for (package_name in packages) {
    if (!requireNamespace(package_name, quietly = TRUE)) {
      install.packages(package_name, repos = "https://cloud.r-project.org")
    }

    suppressPackageStartupMessages(
      library(package_name, character.only = TRUE)
    )
  }
}

get_script_dir <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  file_argument <- "--file="
  script_path <- sub(file_argument, "", args[grep(file_argument, args)])

  if (length(script_path) > 0) {
    return(dirname(normalizePath(script_path[1], winslash = "/")))
  }

  normalizePath(getwd(), winslash = "/")
}

ensure_dir <- function(path) {
  dir.create(path, recursive = TRUE, showWarnings = FALSE)
}

rescale_to_100 <- function(values) {
  minimum <- min(values, na.rm = TRUE)
  maximum <- max(values, na.rm = TRUE)

  if (identical(minimum, maximum)) {
    return(rep(100, length(values)))
  }

  round(((values - minimum) / (maximum - minimum)) * 100, 1)
}

round_numeric_columns <- function(data, digits = 4) {
  data |>
    dplyr::mutate(dplyr::across(dplyr::where(is.numeric), ~ round(.x, digits = digits)))
}

bootstrap_packages(c(
  "tidyverse",
  "lubridate",
  "rio",
  "caret",
  "randomForest",
  "jsonlite"
))

script_dir <- get_script_dir()
project_root <- normalizePath(file.path(script_dir, ".."), winslash = "/")

data_raw_dir <- file.path(project_root, "data", "raw")
data_processed_dir <- file.path(project_root, "data", "processed")
output_dir <- file.path(project_root, "outputs", "backend")

ensure_dir(data_processed_dir)
ensure_dir(output_dir)

source(file.path(script_dir, "feature_creation.R"))
source(file.path(script_dir, "model_develop_and_eval.R"))

events_path <- file.path(data_raw_dir, "Events.xlsx")
results_path <- file.path(data_raw_dir, "Results.xlsx")

if (!file.exists(events_path) || !file.exists(results_path)) {
  stop("Expected local dataset files were not found in data/raw. Run the dataset copy step first.")
}

message("Loading local Chapter 07 datasets...")
events <- import(events_path)
results <- import(results_path)

message("Preparing event data...")
events <- events |>
  arrange(timecreated) |>
  mutate(
    wday = wday(
      timecreated,
      label = TRUE,
      abbr = TRUE,
      week_start = 1
    ),
    prev_wday = lag(wday),
    new_week = ifelse(
      (wday == "Mon") & (is.na(prev_wday) | prev_wday != "Mon"),
      yes = TRUE,
      no = FALSE
    ),
    course_week = cumsum(new_week)
  ) |>
  select(-c(wday, prev_wday, new_week))

topical_action <- c("General", "Applications", "Theory", "Ethics", "Feedback", "La_types")

events <- events |>
  mutate(
    action = ifelse(
      test = Action %in% topical_action,
      yes = str_glue("Materials_{Action}"),
      no = Action
    ),
    .keep = "unused"
  ) |>
  select(user, timecreated, course_week, action) |>
  rename(week = course_week, ts = timecreated) |>
  mutate(date = as.Date(ts))

events_with_sessions <- events |>
  group_by(user) |>
  arrange(ts, .by_group = TRUE) |>
  mutate(ts_diff = ts - lag(ts)) |>
  ungroup() |>
  mutate(ts_diff_hours = as.numeric(ts_diff, units = "hours")) |>
  group_by(user) |>
  arrange(ts, .by_group = TRUE) |>
  mutate(
    new_session = is.na(ts_diff_hours) | ts_diff_hours >= 1.5,
    session_nr = cumsum(new_session),
    session_id = paste0(user, "_session_", session_nr)
  ) |>
  ungroup() |>
  group_by(session_id) |>
  mutate(session_len = as.numeric(max(ts) - min(ts), units = "secs")) |>
  ungroup() |>
  select(user, ts, date, week, action, session_nr, session_id, session_len)

message("Preparing result data...")
results <- results |>
  mutate(
    Course_outcome = ifelse(
      test = Final_grade > median(Final_grade),
      yes = "High",
      no = "Low"
    ),
    Course_outcome = factor(Course_outcome, levels = c("High", "Low"))
  ) |>
  select(user, Final_grade, Course_outcome)

write_csv(events, file.path(data_processed_dir, "events.csv"))
write_csv(events_with_sessions, file.path(data_processed_dir, "events_with_sessions.csv"))
write_csv(results, file.path(data_processed_dir, "final_grades.csv"))

message("Training classification models...")
classification_evaluations <- vector("list", 5)

for (current_week in 1:5) {
  weekly_dataset <- create_dataset_for_course_success_prediction(
    events_with_sessions,
    current_week,
    results
  )

  set.seed(2023)
  train_indices <- createDataPartition(
    weekly_dataset$Course_outcome,
    p = 0.8,
    list = FALSE
  )

  train_data <- weekly_dataset[train_indices, ] |>
    select(-user)
  test_data <- weekly_dataset[-train_indices, ] |>
    select(-user)

  weekly_model <- build_RF_classification_model(train_data)
  weekly_metrics <- get_classification_evaluation_measures(weekly_model, test_data)

  classification_evaluations[[current_week]] <- tibble(
    week = current_week,
    Accuracy = weekly_metrics[["Accuracy"]],
    Precision = weekly_metrics[["Precision"]],
    Recall = weekly_metrics[["Recall"]],
    F1 = weekly_metrics[["F1"]]
  )
}

classification_metrics <- bind_rows(classification_evaluations)
best_classification_week <- classification_metrics |>
  arrange(desc(F1), desc(Accuracy)) |>
  slice(1) |>
  pull(week)

message(str_glue("Best classification week: {best_classification_week}"))

full_classification_dataset <- create_dataset_for_course_success_prediction(
  events_with_sessions,
  best_classification_week,
  results
)

full_classification_model <- build_RF_classification_model(
  full_classification_dataset |>
    select(-user)
)

classification_probabilities <- predict(
  full_classification_model,
  full_classification_dataset |>
    select(-user, -Course_outcome),
  type = "prob"
)

risk_probability <- unname(classification_probabilities[, "Low"])
predicted_outcome <- ifelse(risk_probability >= 0.5, "Low", "High")

message("Training regression models...")
regression_evaluations <- vector("list", 5)

for (current_week in 1:5) {
  weekly_dataset <- create_dataset_for_grade_prediction(
    events_with_sessions,
    current_week,
    results
  )

  set.seed(2023)
  train_indices <- createDataPartition(
    weekly_dataset$Final_grade,
    p = 0.8,
    list = FALSE
  )

  train_data <- weekly_dataset[train_indices, ] |>
    select(-user)
  test_data <- weekly_dataset[-train_indices, ] |>
    select(-user)

  weekly_model <- build_RF_regression_model(train_data)
  weekly_metrics <- get_regression_evaluation_measures(weekly_model, train_data, test_data)

  regression_evaluations[[current_week]] <- tibble(
    week = current_week,
    R2 = weekly_metrics[["R2"]],
    RMSE = weekly_metrics[["RMSE"]],
    MAE = weekly_metrics[["MAE"]]
  )
}

regression_metrics <- bind_rows(regression_evaluations)
best_regression_week <- regression_metrics |>
  arrange(desc(R2), RMSE) |>
  slice(1) |>
  pull(week)

message(str_glue("Best regression week: {best_regression_week}"))

full_regression_dataset <- create_dataset_for_grade_prediction(
  events_with_sessions,
  best_regression_week,
  results
)

full_regression_model <- build_RF_regression_model(
  full_regression_dataset |>
    select(-user)
)

predicted_grade <- predict(
  full_regression_model,
  full_regression_dataset |>
    select(-user, -Final_grade)
)

classification_importance <- extract_variable_importance(
  full_classification_model,
  "classification",
  top_n = 10
)
regression_importance <- extract_variable_importance(
  full_regression_model,
  "regression",
  top_n = 10
)

count_columns <- names(full_classification_dataset)[grepl("_cnt$", names(full_classification_dataset))]

activity_summary <- full_classification_dataset |>
  select(user, all_of(count_columns)) |>
  mutate(activity_total = rowSums(across(all_of(count_columns)), na.rm = TRUE)) |>
  select(user, activity_total)

last_login <- events_with_sessions |>
  filter(week <= best_classification_week) |>
  group_by(user) |>
  summarise(last_login = as.character(max(ts)), .groups = "drop")

student_predictions <- full_classification_dataset |>
  select(user) |>
  distinct() |>
  left_join(last_login, by = "user") |>
  left_join(
    tibble(
      user = full_classification_dataset$user,
      risk_probability = risk_probability,
      predicted_outcome = predicted_outcome
    ),
    by = "user"
  ) |>
  left_join(
    tibble(
      user = full_regression_dataset$user,
      predicted_grade = as.numeric(predicted_grade)
    ),
    by = "user"
  ) |>
  left_join(activity_summary, by = "user") |>
  mutate(
    name = user,
    activity_score = rescale_to_100(activity_total),
    risk_level = case_when(
      risk_probability >= 0.66 ~ "high",
      risk_probability >= 0.33 ~ "medium",
      TRUE ~ "low"
    )
  ) |>
  arrange(desc(risk_probability)) |>
  select(
    user,
    name,
    risk_level,
    risk_probability,
    predicted_outcome,
    predicted_grade,
    activity_score,
    last_login
  )

risk_counts <- student_predictions |>
  count(risk_level, name = "count") |>
  arrange(desc(count))

classification_metrics_out <- round_numeric_columns(classification_metrics, digits = 4)
regression_metrics_out <- round_numeric_columns(regression_metrics, digits = 4)
classification_importance_out <- round_numeric_columns(classification_importance, digits = 4)
regression_importance_out <- round_numeric_columns(regression_importance, digits = 4)
student_predictions_out <- student_predictions |>
  mutate(
    risk_probability = round(risk_probability, 4),
    predicted_grade = round(predicted_grade, 2),
    activity_score = round(activity_score, 1)
  )

write_csv(
  classification_metrics_out,
  file.path(output_dir, "classification_metrics_by_week.csv")
)
write_csv(
  regression_metrics_out,
  file.path(output_dir, "regression_metrics_by_week.csv")
)
write_csv(
  classification_importance_out,
  file.path(output_dir, "feature_importance_classification.csv")
)
write_csv(
  regression_importance_out,
  file.path(output_dir, "feature_importance_regression.csv")
)
write_csv(
  student_predictions_out,
  file.path(output_dir, "student_predictions.csv")
)

saveRDS(full_classification_model, file.path(output_dir, "best_classification_model.rds"))
saveRDS(full_regression_model, file.path(output_dir, "best_regression_model.rds"))

dashboard_payload <- list(
  project = list(
    title = "Student Success Prediction Dashboard",
    generated_at = format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
    backend = "R",
    source_chapter = "Chapter 07"
  ),
  overview = list(
    total_students = nrow(student_predictions_out),
    high_risk = student_predictions_out |>
      filter(risk_level == "high") |>
      nrow(),
    medium_risk = student_predictions_out |>
      filter(risk_level == "medium") |>
      nrow(),
    low_risk = student_predictions_out |>
      filter(risk_level == "low") |>
      nrow(),
    best_classification_week = best_classification_week,
    best_regression_week = best_regression_week
  ),
  risk_counts = risk_counts,
  classification_metrics = classification_metrics_out,
  regression_metrics = regression_metrics_out,
  top_features = list(
    classification = classification_importance_out,
    regression = regression_importance_out
  ),
  students = student_predictions_out
)

write_json(
  dashboard_payload,
  file.path(output_dir, "dashboard.json"),
  pretty = TRUE,
  auto_unbox = TRUE,
  dataframe = "rows"
)

message("FYP Chapter 07 backend outputs generated successfully.")