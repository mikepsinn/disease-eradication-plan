# Data Dictionary & Database Schema

**Status:** DRAFT
**Version:** 0.2

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

## `users`

Stores information about individual users of the platform.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `UUID` | **Primary Key.** |
| `did` | `TEXT` | **Unique.** The user's Decentralized Identifier (DID). |
| `created_at`| `TIMESTAMPTZ` | Timestamp of account creation. |
| `updated_at`| `TIMESTAMPTZ` | Timestamp of the last update. |

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
| `default_unit_id` | `UUID` | Foreign key referencing the `units` table. |
| `is_input` | `BOOLEAN`| `true` if the variable can be considered a controllable input factor. |
| `is_outcome`| `BOOLEAN` | `true` if the variable can be considered a health outcome. |

## `units`

Contains definitions for all units of measurement, based on UCUM.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `UUID` | **Primary Key.** |
| `ucum_code` | `TEXT` | **Unique.** The Unified Code for Units of Measure (UCUM) code (e.g., "mm[Hg]"). |
| `name` | `TEXT` | The common name of the unit (e.g., "Millimeters of Mercury"). |
| `description`| `TEXT` | A description of the unit. |

## `sources`

Describes the origin of data (e.g., a specific app, device, plugin, or manual entry).

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `UUID` | **Primary Key.** |
| `name` | `TEXT` | The name of the data source (e.g., "Fitbit API Plugin", "Manual Entry Form"). |
| `description`| `TEXT` | A description of the source. |
| `is_active` | `BOOLEAN` | `false` if the source is disabled or deprecated. |

## `consents`

Logs all consent actions taken by users, providing an auditable trail.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `UUID` | **Primary Key.** |
| `user_id` | `UUID` | Foreign key referencing the `users` table. |
| `trial_id` | `UUID` | Foreign key referencing the `trials` table. |
| `granted_at`| `TIMESTAMPTZ` | The timestamp when the consent was granted. |
| `revoked_at`| `TIMESTAMPTZ` | The timestamp when the consent was revoked (if applicable). |
| `document_hash` | `TEXT` | A cryptographic hash of the exact consent document version that was signed. |
| `quiz_passed` | `BOOLEAN` | `true` if the user successfully passed the comprehension quiz. |

## `trials`

Contains information about each clinical trial managed on the platform.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `UUID` | **Primary Key.** |
| `creator_id`| `UUID` | Foreign key referencing the `users` table of the trial creator. |
| `protocol_id`|`TEXT` | An identifier for the registered e-protocol document. |
| `name` | `TEXT` | The official name of the trial. |
| `status` | `TEXT` | The current status (e.g., "Recruiting", "Active", "Completed", "Halted"). |
| `created_at`| `TIMESTAMPTZ`| Timestamp of trial creation. |

---
*This is a simplified representation. The full schema will be maintained here as it is developed.*
