# Data Dictionary & Database Schema

**Status:** DRAFT
**Version:** 0.1

This document provides a detailed description of the database schema used in the platform's core relational database (PostgreSQL).

---

## `observations` (Hypertable)

This is the main time-series table for storing all quantitative health data.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `timestamp` | `TIMESTAMPTZ` | **Primary Key.** The exact time the observation was recorded. |
| `user_id` | `UUID` | **Primary Key.** Foreign key referencing the `users` table. |
| `variable_id` | `UUID` | **Primary Key.** Foreign key referencing the `variables` definition table. |
| `value` | `FLOAT` | The numerical value of the observation. |
| `unit_id` | `UUID` | Foreign key referencing the `units` definition table. |
| `source_id` | `UUID` | Foreign key referencing the `sources` table (e.g., a specific app, device, or lab). |
| `is_valid` | `BOOLEAN` | A flag set by the validation engine. `true` if the data point passed all quality checks. |
| `is_outlier`| `BOOLEAN` | A flag set by the validation engine if the value is considered an outlier. |
| `metadata` | `JSONB` | A flexible field for storing additional source-specific context. |

## `variables`

This table contains the definitions for all measurable variables in the system.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `UUID` | **Primary Key.** |
| `name` | `TEXT` | The common name of the variable (e.g., "Heart Rate"). |
| `description`| `TEXT` | A detailed description of the variable. |
| `category` | `TEXT` | A category for grouping (e.g., "Vital Sign", "Lab Result"). |
| `min_value` | `FLOAT` | The minimum plausible physiological value. |
| `max_value` | `FLOAT` | The maximum plausible physiological value. |
| `default_unit_id` | `UUID` | The standard unit for this variable. |
| `is_input` | `BOOLEAN`| `true` if the variable can be considered a controllable input factor. |
| `is_outcome`| `BOOLEAN` | `true` if the variable can be considered a health outcome. |

---
*This is a simplified representation. The full schema will be maintained here as it is developed.* 