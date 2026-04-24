build_RF_classification_model <- function(dataset) {
  n_features <- ncol(dataset) - 1
  default_mtry <- round(sqrt(n_features))
  grid <- expand.grid(.mtry = (default_mtry - 1):(default_mtry + 1))

  ctrl <- trainControl(
    method = "CV",
    number = 10,
    classProbs = TRUE,
    summaryFunction = twoClassSummary
  )

  rf <- train(
    x = dataset |>
      select(-Course_outcome),
    y = dataset$Course_outcome,
    method = "rf",
    metric = "ROC",
    tuneGrid = grid,
    trControl = ctrl
  )

  rf$finalModel
}

get_classification_evaluation_measures <- function(model, test_data) {
  predicted_vals <- predict(model, test_data |>
    select(-Course_outcome))
  actual_vals <- test_data$Course_outcome

  cm <- table(actual_vals, predicted_vals)

  tp <- cm[2, 2]
  tn <- cm[1, 1]
  fp <- cm[1, 2]
  fn <- cm[2, 1]

  accuracy <- sum(diag(cm)) / sum(cm)
  precision <- tp / (tp + fp)
  recall <- tp / (tp + fn)
  f1 <- (2 * precision * recall) / (precision + recall)

  c(
    Accuracy = accuracy,
    Precision = precision,
    Recall = recall,
    F1 = f1,
    TrueNegative = tn,
    FalsePositive = fp,
    FalseNegative = fn,
    TruePositive = tp
  )
}

build_RF_regression_model <- function(dataset) {
  n_features <- ncol(dataset) - 1
  default_mtry <- round(sqrt(n_features))
  grid <- expand.grid(.mtry = (default_mtry - 1):(default_mtry + 1))

  ctrl <- trainControl(
    method = "CV",
    number = 10
  )

  rf <- train(
    x = dataset |>
      select(-Final_grade),
    y = dataset$Final_grade,
    method = "rf",
    metric = "RMSE",
    tuneGrid = grid,
    trControl = ctrl
  )

  rf$finalModel
}

get_regression_evaluation_measures <- function(model, train_data, test_data) {
  predicted_vals <- predict(model, test_data |>
    select(-Final_grade))
  actual_vals <- test_data$Final_grade

  rss <- sum((predicted_vals - actual_vals)^2)
  tss <- sum((median(train_data$Final_grade) - actual_vals)^2)
  r2 <- 1 - rss / tss
  rmse <- sqrt(rss / nrow(test_data))
  mae <- mean(abs(predicted_vals - actual_vals))

  c(R2 = r2, RMSE = rmse, MAE = mae)
}

extract_variable_importance <- function(model, label, top_n = 10) {
  importance_df <- importance(model, type = 2) |>
    as.data.frame()

  numeric_columns <- names(importance_df)[vapply(importance_df, is.numeric, logical(1))]
  importance_column <- numeric_columns[1]

  tibble(
    feature = rownames(importance_df),
    importance = importance_df[[importance_column]],
    model = label
  ) |>
    arrange(desc(importance)) |>
    slice_head(n = top_n)
}