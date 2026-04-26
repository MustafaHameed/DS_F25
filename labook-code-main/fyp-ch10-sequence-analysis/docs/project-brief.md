# Project Brief

## Domain

Learning analytics, sequence analysis, and session pattern discovery.

## System Summary

This project translates the Chapter 10 sequence-analysis workflow into a Python-first FYP. It transforms Moodle logs into session traces, clusters those traces into typical learning-session patterns, and allows a user to enter a new session sequence for manual cluster matching.

## Core Modules

1. Moodle event-log loading from a local data copy.
2. Sessionization with a 15-minute inactivity rule.
3. Sequence-table construction with a fixed-length representation.
4. Sequence clustering and validation.
5. Manual-input web demo for cluster assignment.