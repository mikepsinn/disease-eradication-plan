---
title: Platform Technical Specification
description: Detailed engineering specifications for the dFDA core platform implementation.
published: false
date: 2025-07-26T14:00:00.000Z
tags: features, platform, specification, engineering
editor: markdown
dateCreated: 2025-07-26T14:00:00.000Z
---

# Platform Technical Specification

**Status:** Draft / Elaboration in Progress
**Version:** 0.1.0

This document provides the detailed technical specifications for the implementation of the dFDA core platform, as outlined conceptually in the [Platform Architecture document](/features/platform/03-platform.md). It is intended for engineers, developers, and technical teams involved in building and maintaining the platform.

**Note:** This document contains illustrative technical choices based on common practices and high-level requirements. Specific technologies, configurations, and details require further analysis, validation, and potential revision based on detailed non-functional requirements and implementation constraints.

## 1. Introduction

*   **Purpose:** To define the specific technologies, interfaces, data structures, security measures, and infrastructure requirements for building the dFDA Core Platform.
*   **Relationship:** Serves as the detailed implementation guide based on the architecture described in `/features/platform/03-platform.md`.
*   **Scope:** Focuses on the Core Platform components (API, Storage, Mapping/Validation, Access Control, Reference Data) and the interfaces for the Plugin Framework. Excludes the internal implementation details of specific plugins.

## 2. Technology Stack

This section outlines the primary technologies selected for the platform. Rationale is provided briefly; detailed trade-off analysis is outside the current scope.

*   **Programming Languages:**
    *   Backend/API: **Python 3.11+** (Leveraging frameworks like FastAPI/Django for rapid development, strong library support for data science/validation, async capabilities). Alternative: Node.js/TypeScript.
    *   Frontend (Reference UI/Dashboards): **TypeScript** with **React 18+** (Component-based architecture, large community, mature tooling).
    *   Data Processing/Mapping Engine: **Python 3.11+** (Strong data manipulation libraries like Pandas, Dask for potential scaling).
*   **Frameworks:**
    *   Web API: **FastAPI** (High performance, automatic data validation via Pydantic, OpenAPI generation). Alternative: Django Rest Framework.
    *   Web Frontend: **Next.js** (Server-side rendering, routing, build optimizations for React).
    *   Data Processing: Standard Python libraries initially; potentially **Apache Spark** or **Dask** if large-scale distributed processing becomes necessary.
*   **Database Technologies:**
    *   Metadata / Relational Storage: **PostgreSQL 15+** (Robust, ACID compliant, strong JSONB support, mature extensions like PostGIS if needed). Hosted via managed service (e.g., AWS RDS, Google Cloud SQL).
    *   Time-Series Data Storage: **TimescaleDB** (PostgreSQL extension optimized for time-series data, leverages mature PostgreSQL ecosystem). Alternative: InfluxDB, Cassandra (if extreme write scale is primary driver). Hosted via managed service or self-managed on cloud VMs.
    *   Raw Data / File Storage: **AWS S3** (Scalable, durable, cost-effective object storage). Alternatives: Google Cloud Storage, Azure Blob Storage.
*   **Cloud Provider & Core Services:**
    *   Primary Cloud Provider: **AWS** (Mature services, broad adoption, extensive documentation). Alternatives: GCP, Azure.
    *   Compute: **AWS EC2** (for potential self-managed DBs/services), **AWS Lambda** (for serverless functions/APIs), **AWS EKS** (for container orchestration).
    *   Storage: **AWS S3**, **AWS RDS (PostgreSQL)**, Managed **TimescaleDB** (e.g., on AWS EC2 or via Timescale Cloud), **AWS EBS**.
    *   Networking: **AWS VPC**, **API Gateway**, **Route 53**, **CloudFront (CDN)**.
    *   Messaging Queues: **AWS SQS** (Simple Queue Service) or **RabbitMQ** hosted on EC2/EKS (for asynchronous job processing - data mapping, validation). Alternative: Kafka (if high-throughput streaming is key).
*   **Containerization & Orchestration:**
    *   Containerization: **Docker**.
    *   Orchestration: **Kubernetes (AWS EKS)** (Standard for managing containerized applications at scale).
*   **Blockchain/Distributed Ledger Technology (DLT):**
    *   **Status:** Exploration Phase. Not core to initial MVP functionality but considered for specific use cases like immutable consent logging or data integrity verification (e.g., timestamping data hashes).
    *   Potential Choices (if implemented): Hyperledger Fabric, Ethereum (Private Network), or specialized verifiable credential frameworks. Requires separate detailed specification.
*   **Monitoring & Logging Tools:**
    *   Logging: **Elasticsearch, Fluentd, Kibana (EFK stack)** deployed on EKS, or Cloud-native solution like **AWS CloudWatch Logs**.
    *   Monitoring/Metrics: **Prometheus** & **Grafana** deployed on EKS, or **AWS CloudWatch Metrics**.
    *   APM: **Datadog**, **New Relic**, or **AWS X-Ray**.
    *   Error Tracking: **Sentry**.

## 3. Core Component Implementation Details

### 3.1 Data Ingestion API

*   **API Protocol:** **RESTful API** using JSON payloads.
*   **Specification:** **OpenAPI Specification (OAS) v3.x**. Auto-generated via FastAPI, manually augmented with detailed descriptions and examples. Hosted and versioned.
*   **Authentication:** **OAuth 2.0 Bearer Tokens** (Client Credentials flow for M2M integration, Authorization Code flow for user-facing apps). Handled via dedicated Authentication service (see 3.4).
*   **Core Endpoints (Illustrative):**
    *   `POST /v1/ingest/observations`: Endpoint for submitting structured time-series data conforming to the internal standardized schema (see 3.2). Supports batch submissions.
    *   `POST /v1/ingest/files`: Endpoint for uploading raw files (CSV, PDF, VCF, etc.). Returns a file ID for later processing. Uses multipart/form-data.
    *   `GET /v1/ingest/jobs/{job_id}`: Check status of asynchronous mapping/validation jobs.
    *   `GET /v1/variables`: Retrieve reference variable definitions.
    *   `GET /v1/units`: Retrieve reference unit definitions.
*   **Data Validation Rules (Server-side):**
    *   Schema Validation: Enforced by FastAPI/Pydantic based on OpenAPI spec. Checks data types, required fields.
    *   Value Range Validation: Check against defined min/max values in the Reference Data Definitions (see 3.5). Configurable enforcement (flag vs. reject).
    *   Unit Validation: Check against allowed units for a given variable code (UCUM where applicable).
    *   Duplicate Check: Prevent insertion of data with identical `(user_id, variable_code, timestamp, source_id)` composite key.
*   **SDK Design:**
    *   Initial Target Languages: **Python**, **JavaScript/TypeScript**.
    *   Core Functionalities: Authentication handling, API request formation for data/file submission, status checking, potentially local validation helpers.
    *   Distribution: PyPI, npm. Open source.

### 3.2 Data Storage

*   **Raw Data Storage (AWS S3):**
    *   Bucket Structure: e.g., `s3://dfda-raw-data-{env}/{user_id}/{source_type}/{yyyy}/{mm}/{dd}/{file_uuid}.{ext}`
    *   Encryption: Server-Side Encryption with AWS KMS managed keys (SSE-KMS) enabled by default. Client-side encryption option available via SDK.
    *   Access Control: IAM policies restricting access to specific services (Ingestion API, Mapping Engine). User-level access mediated strictly through platform APIs. Versioning enabled.
*   **Time-Series Data Storage (TimescaleDB on Managed PostgreSQL):**
    *   Primary Table (`observations` Hypertable):
        *   `user_id`: UUID (Foreign Key to Users table)
        *   `timestamp`: TIMESTAMPTZ (Primary time index)
        *   `variable_id`: INT (Foreign Key to Variables table)
        *   `value_numeric`: DOUBLE PRECISION (For numeric values)
        *   `value_text`: TEXT (For categorical or text values)
        *   `unit_id`: INT (Foreign Key to Units table)
        *   `source_id`: INT (Foreign Key to Sources table)
        *   `raw_file_id`: UUID (Optional, links to raw file if applicable)
        *   `ingestion_job_id`: UUID
        *   `is_valid`: BOOLEAN (Result of validation)
        *   `is_outlier`: BOOLEAN (Flagged by analysis)
        *   `metadata`: JSONB (Additional context, e.g., device info, specific FHIR resource details)
    *   Partitioning: Automatic partitioning by `timestamp` (e.g., daily or weekly chunks) managed by TimescaleDB. Potential secondary partitioning/indexing on `user_id` and `variable_id`.
    *   Indexes: Composite index on `(user_id, variable_id, timestamp DESC)`. Additional indexes as needed based on query patterns.
    *   Data Retention: Policies defined per environment (e.g., Production retains indefinitely with potential tiered storage/archiving to S3 via TimescaleDB features; Staging/Dev prune older data).
    *   Backup: Managed by cloud provider (e.g., AWS RDS automated backups, point-in-time recovery).
*   **Metadata / Relational Storage (PostgreSQL):**
    *   Key Tables: `users`, `oauth_clients`, `permissions`, `roles`, `consents`, `variables`, `units`, `sources`, `plugins`, `ingestion_jobs`, etc.
    *   Schema: Detailed ERD and CREATE TABLE statements maintained separately [See Appendix X]. Focus on normalization, referential integrity. Use of UUIDs for primary keys where appropriate. JSONB for flexible metadata storage.

### 3.3 Data Mapping & Validation Engine

*   **Implementation:** Set of containerized **Python microservices** managed by Kubernetes (EKS). Triggered via messages on **AWS SQS**.
*   **Mapping Logic:**
    *   Separate mapping functions/classes per input format/standard (FHIR Resource X, specific CSV format, specific device API).
    *   Core mappers (FHIR Patient, Observation, Condition; LOINC codes; SNOMED codes; common EHR formats) maintained by core team.
    *   Plugin system allows third parties to register new mappers.
    *   Utilizes the `variables` and `units` reference tables (see 3.5) to map source codes/units to internal IDs.
*   **Validation Logic:**
    *   Separate validation service called after mapping.
    *   Applies rules defined in 3.1 (schema, range, unit, duplication).
    *   Flags data (`is_valid`, `is_outlier`) rather than rejecting outright where appropriate (configurable).
*   **Error Handling:** Failed mapping/validation attempts logged comprehensively (Input data snippet, error type, timestamp). Notifications sent to monitoring system (e.g., Sentry) and potentially back to the source system/user via API status checks or dedicated notification system. Dead-letter queue configured in SQS.
*   **Asynchronous Queue (SQS):** Separate queues for different job types (e.g., `file-processing-queue`, `api-ingestion-queue`) with appropriate visibility timeouts and retry mechanisms.

### 3.4 Data Ownership & Access Control

*   **Authentication:** Dedicated **OAuth 2.0 / OpenID Connect (OIDC) service** (e.g., using Hydra, Keycloak, or cloud provider service like AWS Cognito). Issues JWTs for API access. Supports standard flows (Authorization Code + PKCE for user apps, Client Credentials for backend services).
*   **Authorization:** Primarily **Role-Based Access Control (RBAC)** for broad permissions (e.g., `data_owner`, `researcher`, `clinician`, `admin`). Complemented by **Attribute-Based Access Control (ABAC)** for fine-grained data access based on consent and policies (e.g., access allowed only to specific variable categories, for a specific time window, for users consenting to Study X). Implemented via middleware in the API gateway or backend services, referencing user roles and consent records.
*   **Permission Management:** API endpoints for users to view/manage connected apps (`oauth_clients`), grant/revoke consents, and potentially define fine-grained sharing rules (persisted in `consents` or dedicated policy tables).
*   **Consent Implementation:** Dedicated `consents` table storing `user_id`, `grantee_id` (can be client app ID or researcher ID), `scope` (e.g., specific data categories, study ID), `start_date`, `expiry_date`, `status` (active, revoked), reference to consent document hash.
*   **Auditing:** Comprehensive audit trail logged (e.g., to dedicated table or CloudWatch Logs) for all sensitive actions: logins, token issuance, permission changes, consent actions, data access requests (success/failure).

### 3.5 Reference Data Management

*   **Storage:** Dedicated tables within the primary **PostgreSQL** database (e.g., `variables`, `units`, `sources`, `ontologies`).
*   **Content:**
    *   `variables`: `variable_id`, `code_system` (e.g., 'LOINC', 'SNOMED', 'INTERNAL'), `code_value`, `display_name`, `description`, `data_type` (numeric, text, categorical), `allowed_units` (JSONB array of unit_ids), `min_value`, `max_value`, `category` (e.g., 'vitals', 'labs', 'genomics', 'survey'), `is_outcome_variable`, `is_input_factor`.
    *   `units`: `unit_id`, `ucum_code`, `display_name`, `description`. Pre-populated based on UCUM standard.
    *   `sources`: `source_id`, `name`, `type` (e.g., 'ehr', 'wearable', 'app', 'user_reported'), `vendor`.
*   **Updates & Versioning:** Controlled updates via administrative interface or documented migration scripts. Consider strategies for versioning variable definitions if meanings change significantly over time while preserving historical data context (e.g., adding valid_from/valid_to timestamps or linking observations to specific definition versions).

## 4. Plugin Framework Interfaces

*   **API Specs:** Defined using **OpenAPI Specification (OAS) v3.x** for interactions between plugins and the Core Platform.
    *   *Core -> Plugin:* Core may call plugin endpoints for tasks like data mapping, analysis, or visualization. Requires plugins to expose standardized endpoints.
    *   *Plugin -> Core:* Plugins utilize the Core Data Ingestion and Data Retrieval APIs (defined in 3.1 and a separate Data Retrieval API spec) using standard OAuth tokens obtained via user consent flows.
*   **Data Formats:** Primarily **JSON** for API interactions. Standardized internal data representation (based on core DB schema) used for analysis plugins.
*   **Security:** Plugins run in isolated environments (e.g., separate containers/serverless functions). Communication secured via HTTPS and standard OAuth tokens. Core platform validates plugin requests and enforces user permissions/consents before granting data access. Plugins must request specific permission scopes during user authorization.
*   **Registration/Discovery:** Central **Plugin Registry** (database table or dedicated service) stores metadata about installed plugins (name, version, developer, required permissions, exposed endpoints, UI components). Core platform uses this for discovery and routing.

## 5. Security Implementation

*   **Network Security:** Strict AWS Security Groups and Network ACLs. Use of private subnets for databases and backend services. API Gateway for public endpoint exposure. VPC Endpoints for internal service communication where possible. WAF (Web Application Firewall) deployed.
*   **Application Security:** Input validation at API gateway and service level. Regular static (SAST) and dynamic (DAST) security testing. Dependency vulnerability scanning (e.g., Snyk, Dependabot). Secure coding practices enforced. Rate limiting and request throttling implemented.
*   **Data Security:**
    *   Encryption: TLS 1.2+ for data in transit. SSE-KMS for data at rest in S3. Transparent Data Encryption (TDE) for PostgreSQL/TimescaleDB where available/required by cloud provider. Application-level encryption for specific sensitive fields if necessary.
    *   Key Management: AWS KMS for managing encryption keys.
    *   Access Control: Principle of Least Privilege applied to all IAM roles and database permissions.
*   **Authentication & Authorization:** Multi-Factor Authentication (MFA) enforced for administrators and recommended for all users. Short-lived access tokens with refresh token rotation. Strict validation of token scopes. Centralized authorization logic.
*   **Compliance:** Infrastructure and processes designed to meet **HIPAA** and **GDPR** technical safeguard requirements (auditing, access controls, encryption, backup/recovery, data minimization principles applied where feasible). Regular compliance audits.
*   **Incident Response:** Documented Incident Response Plan including detection, containment, eradication, recovery, and post-mortem phases. [See Separate Incident Response Plan Document].

## 6. Infrastructure & Deployment

*   **Infrastructure as Code (IaC):** **Terraform** used to define and manage all cloud infrastructure resources. State files managed securely.
*   **CI/CD Pipeline:** **GitLab CI/CD** or **GitHub Actions**. Pipeline includes linting, unit testing, integration testing, security scanning (SAST, dependencies), container building/pushing, and automated deployment to respective environments.
*   **Environments:** Separate, isolated environments for `development`, `staging`, and `production` (potentially more, e.g., `qa`). Staging mirrors production infrastructure closely.
*   **Scalability Strategy:**
    *   Stateless Services: Design backend APIs and processing services to be stateless for horizontal scaling.
    *   Auto-scaling: Configure Kubernetes Horizontal Pod Autoscaler (HPA) and AWS Auto Scaling Groups based on CPU/Memory utilization or custom metrics (e.g., queue length).
    *   Database Scaling: Vertical scaling (instance size) for PostgreSQL/TimescaleDB initially. Read replicas for PostgreSQL. Investigate TimescaleDB clustering/multi-node capabilities if write/read load exceeds single-node limits. S3 scales automatically.
    *   Load Balancing: AWS Application Load Balancer (ALB) in front of API services.
*   **Disaster Recovery:** Regular automated backups (see 3.2). Plan for cross-region replication of critical data (S3, database backups) and ability to redeploy infrastructure via IaC in a secondary region. Defined RPO (Recovery Point Objective) and RTO (Recovery Time Objective). [See Separate Disaster Recovery Plan Document].

## 7. Performance & Scalability Requirements

*(Note: These are illustrative placeholders and require detailed analysis based on expected usage)*

*   **Expected Load:**
    *   Users: Target 1 Million MAU (Monthly Active Users) within 2 years, scaling to 100M+ L TBD.
    *   Data Volume: Ingestion rate of [X] TB/month. Total storage [Y] PB within 5 years.
    *   API Calls: Peak [Z] requests per second.
*   **Latency Requirements:**
    *   Core API (Read/Write): p95 latency < 200ms.
    *   Data Ingestion (Async): Job acknowledged < 50ms; Processing time varies (target p95 < 5 minutes for typical files/batches).
*   **Throughput Requirements:**
    *   Ingestion: Support sustained [A] observations/second.
    *   Data Retrieval API: Support [B] concurrent analytical queries.
*   **Scalability Targets:** System designed to scale horizontally to handle 10x projected peak load with acceptable performance degradation.

## 8. Appendices

*(Placeholders - Content to be generated separately or by human teams)*

*   **Glossary of Technical Terms:** [Link to Glossary]
*   **Detailed Diagrams:**
    *   System Architecture Diagram [Link]
    *   Data Flow Diagrams [Link]
    *   Sequence Diagrams (Key Workflows) [Link]
    *   Deployment Diagram [Link]
*   **Data Dictionary / Database Schema:** [Link to ERD and DDL Scripts]
*   **API Specifications (OAS Files):** [Link to OAS Files/Repository]

---

*This specification is a living document and will be updated as technical decisions are made and implementation progresses.* 