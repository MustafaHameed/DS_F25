if (!"package:dplyr" %in% search()) {
  suppressPackageStartupMessages(library(dplyr))
}

if (!"package:tidyr" %in% search()) {
  suppressPackageStartupMessages(library(tidyr))
}

total_counts_per_action_type <- function(events_data, current_week) {
  events_data |>
    filter(.data$week <= current_week) |>
    mutate(action = ifelse(startsWith(.data$action, "Materials"), "Course_materials", .data$action)) |>
    count(.data$user, .data$action) |>
    pivot_wider(
      id_cols = "user",
      names_from = "action",
      names_glue = "{action}_cnt",
      values_from = "n",
      values_fill = 0
    )
}

avg_action_cnt_per_day <- function(events_data, current_week) {
  events_data |>
    filter(.data$week <= current_week) |>
    group_by(.data$user, .data$date) |>
    summarise(daily_action_cnt = dplyr::n(), .groups = "drop") |>
    group_by(.data$user) |>
    summarise(avg_daily_cnt = median(.data$daily_action_cnt), .groups = "drop")
}

daily_cnt_entropy <- function(events_data, current_week) {
  events_data |>
    filter(.data$week <= current_week) |>
    group_by(.data$user) |>
    mutate(tot_action_cnt = dplyr::n()) |>
    ungroup() |>
    group_by(.data$user, .data$date) |>
    reframe(
      daily_action_cnt = dplyr::n(),
      daily_action_prop = dplyr::n() / first(.data$tot_action_cnt)
    ) |>
    ungroup() |>
    group_by(.data$user) |>
    summarise(
      entropy_daily_cnts = -1 * sum(.data$daily_action_prop * log2(.data$daily_action_prop)),
      .groups = "drop"
    )
}

session_based_features <- function(events_data, current_week) {
  session_stats <- events_data |>
    filter(.data$week <= current_week) |>
    distinct(.data$user, .data$session_id, .data$session_len) |>
    group_by(.data$user) |>
    mutate(
      session_cnt = dplyr::n(),
      avg_session_len = median(.data$session_len),
      tot_session_len = sum(.data$session_len)
    ) |>
    ungroup() |>
    group_by(.data$user, .data$session_id) |>
    mutate(session_len_prop = .data$session_len / .data$tot_session_len) |>
    ungroup()

  session_stats |>
    group_by(.data$user) |>
    mutate(session_len_entropy = -1 * sum(.data$session_len_prop * log2(.data$session_len_prop))) |>
    ungroup() |>
    distinct(.data$user, .data$session_cnt, .data$avg_session_len, .data$session_len_entropy)
}

active_days_count <- function(events_data, current_week) {
  events_data |>
    filter(.data$week <= current_week) |>
    group_by(.data$user) |>
    summarise(active_days_cnt = dplyr::n_distinct(.data$date), .groups = "drop")
}

active_days_avg_time_dist <- function(events_data, current_week) {
  avg_aday_dist_df <- events_data |>
    filter(.data$week <= current_week) |>
    distinct(.data$user, .data$date) |>
    group_by(.data$user) |>
    arrange(.data$date, .by_group = TRUE) |>
    mutate(day_dist = as.numeric(.data$date - lag(.data$date), units = "days")) |>
    summarise(avg_aday_dist = median(.data$day_dist, na.rm = TRUE), .groups = "drop")

  max_avg_aday_dist <- max(avg_aday_dist_df$avg_aday_dist, na.rm = TRUE)

  avg_aday_dist_df |>
    mutate(
      avg_aday_dist = ifelse(
        test = is.na(.data$avg_aday_dist),
        yes = max_avg_aday_dist * 2,
        no = .data$avg_aday_dist
      )
    )
}

create_event_based_features <- function(events_data, current_week) {
  f1 <- total_counts_per_action_type(events_data, current_week)
  f2 <- avg_action_cnt_per_day(events_data, current_week)
  f3 <- daily_cnt_entropy(events_data, current_week)
  f4 <- session_based_features(events_data, current_week)
  f5 <- active_days_count(events_data, current_week)
  f6 <- active_days_avg_time_dist(events_data, current_week)

  f1 |>
    inner_join(f2, by = "user") |>
    inner_join(f3, by = "user") |>
    inner_join(f4, by = "user") |>
    inner_join(f5, by = "user") |>
    inner_join(f6, by = "user")
}

create_dataset_for_grade_prediction <- function(events_data, current_week, grades) {
  features <- create_event_based_features(events_data, current_week)

  grades |>
    select(.data$user, .data$Final_grade) |>
    inner_join(features, by = "user")
}

create_dataset_for_course_success_prediction <- function(events_data, current_week, grades) {
  features <- create_event_based_features(events_data, current_week)

  grades |>
    select(.data$user, .data$Course_outcome) |>
    inner_join(features, by = "user")
}