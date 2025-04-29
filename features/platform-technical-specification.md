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

**Status:** Draft / Elaboration Complete (Illustrative)
**Version:** 0.2.0

This document provides detailed technical specifications for the implementation of the dFDA core platform, aligning with the architecture in [/features/platform/03-platform.md](/features/platform/03-platform.md) and enabling functionalities discussed in related documents like [/features/data-import.md](/features/data-import.md), [/features/data-silo-api-gateways.md](/features/data-silo-api-gateways.md), and drawing inspiration from efficiency models like [/reference/recovery-trial.md](/reference/recovery-trial.md). It is intended for engineers, developers, and technical teams.

**Note:** This specification uses **illustrative technical choices** based on common practices for scalable, secure health data platforms. Specific technologies, configurations, and details require further rigorous analysis, prototyping, validation against non-functional requirements (performance, load, budget), and potential revision during development.

## 1. Introduction

*   **Purpose:** To define the specific technologies, interfaces, data structures, security measures, and infrastructure requirements for building the dFDA Core Platform.
*   **Relationship:** Serves as the detailed implementation guide based on the architecture described in `/features/platform/03-platform.md`.
*   **Scope:** Focuses on the Core Platform components (API, Storage, Mapping/Validation, Access Control, Reference Data) and the interfaces for the Plugin Framework. Excludes the internal implementation details of specific plugins. The Core Platform is intended to be developed as **open-source software**. 

## 2. Technology Stack

Selected to prioritize scalability, security, interoperability, developer productivity, and leveraging mature ecosystems suitable for health data.

*   **Programming Languages:**
    *   Backend/API: **Python 3.11+** (FastAPI framework, strong data science/validation libraries (Pandas, Pydantic), mature async support, large talent pool).
    *   Frontend (Reference UI): **TypeScript** with **React 18+** (Robust typing, component model, large ecosystem, Next.js framework).
    *   Data Processing/Mapping Engine: **Python 3.11+** (Leverages Pandas, potentially Dask/Spark for large-scale transformations).
*   **Frameworks:**
    *   Web API: **FastAPI** (Performance, auto-validation, OpenAPI generation).
    *   Web Frontend: **Next.js** (SSR, routing, optimized React development).
    *   Data Processing: Standard Python libraries + **Dask** (for parallelizing mapping/validation jobs where appropriate).
*   **Database Technologies:**
    *   Metadata/Relational Storage: **PostgreSQL 15+ (Managed Service - e.g., AWS RDS)** (ACID compliance, JSONB support, maturity, availability of extensions like PostGIS).
    *   Time-Series Data Storage: **TimescaleDB (Managed Service - e.g., Timescale Cloud or via Managed PostgreSQL)** (Optimized time-series performance on mature PostgreSQL foundation, supports analytical queries).
    *   Raw Data/File Storage: **AWS S3** (Scalability, durability, cost-effectiveness, lifecycle policies, event notifications).
*   **Cloud Provider & Core Services:**
    *   Primary Cloud Provider: **AWS** (Mature, comprehensive services, regulatory compliance support - BAA for HIPAA).
    *   Compute: **AWS EKS** (Kubernetes for container orchestration), **AWS Lambda** (for specific event-driven tasks/APIs), **AWS EC2** (potentially for specialized workloads).
    *   Storage: **AWS S3**, **AWS RDS (PostgreSQL)**, Managed **TimescaleDB**, **AWS EBS**.
    *   Networking: **AWS VPC** (Isolation), **API Gateway** (Management, security), **Route 53** (DNS), **CloudFront** (CDN for frontend/static assets).
    *   Messaging Queues: **AWS SQS** (Decoupled asynchronous processing), potentially **AWS SNS** (Notifications).
*   **Containerization & Orchestration:**
    *   Containerization: **Docker**.
    *   Orchestration: **Kubernetes (AWS EKS)** (Scalability, resilience, standardized deployments).
*   **Blockchain/Distributed Ledger Technology (DLT):**
    *   **Status:** **Not part of Core MVP.** Considered for future plugins/extensions for specific use cases (e.g., immutable consent logs via timestamping hashes on a public ledger, Verifiable Credentials for identity). Requires separate design if pursued.
*   **Monitoring & Logging Tools:**
    *   Logging: **AWS CloudWatch Logs** integrated with **OpenSearch/Elasticsearch** for centralized querying/analysis.
    *   Monitoring/Metrics: **AWS CloudWatch Metrics** & **Prometheus/Grafana** (deployed on EKS for finer-grained infra/app metrics).
    *   APM: **AWS X-Ray** or **Datadog**.
    *   Error Tracking: **Sentry**.

## 3. Core Component Implementation Details

### 3.1 Data Ingestion API

Designed for flexibility, security, and standardization.

*   **API Protocol:** **RESTful API** using JSON payloads.
*   **Specification:** **OpenAPI Specification (OAS) v3.x**. Strictly maintained, versioned, and published. Auto-generated documentation via FastAPI.
*   **Authentication:** **OAuth 2.0 Bearer Tokens** (JWTs) issued by the central Auth Service (see 3.4). Required for all endpoints.
*   **Core Endpoints (Illustrative):**
    *   `POST /v1/ingest/observations`: Submits structured time-series data batches conforming to the internal standardized schema. Returns `job_id` for async processing.
    *   `POST /v1/ingest/files`: Uploads raw files (CSV, PDF, VCF, images etc.) via multipart/form-data. Returns `file_id` and `job_id`.
    *   `GET /v1/ingest/jobs/{job_id}`: Retrieves status and outcome (success, failure, validation issues) of an ingestion job.
    *   `GET /v1/variables?category={cat}&system={sys}&code={code}`: Retrieves reference variable definitions, filterable.
    *   `GET /v1/units?system={sys}`: Retrieves reference unit definitions (e.g., UCUM).
*   **Data Validation Rules (Server-side):**
    *   Schema Validation: Performed by FastAPI/Pydantic against OAS.
    *   Semantic Validation (Async job): Checks against `variables` definition (range, allowed units). Flags (`is_valid=false`) or rejects based on severity/configuration. Checks for temporal consistency where possible.
    *   Duplicate Check (Async job): Prevents data points with identical `(user_id, variable_id, timestamp, source_id)`. Logs duplicates.
*   **SDK Design:**
    *   Targets: **Python**, **JavaScript/TypeScript**. Others based on demand.
    *   Functionality: Handles OAuth flows, request building, file upload streaming, job status polling, reference data lookup.
    *   Distribution: Open source (PyPI, npm).

### 3.2 Data Storage

Layered approach prioritizing raw data integrity and optimized query performance.

*   **Raw Data Storage (AWS S3):**
    *   Bucket Structure: `s3://dfda-raw-data-{env}/{user_id_hash_prefix}/{user_id}/{source_type}/{yyyy}/{mm}/{dd}/{file_uuid}.{ext}` (Hashing prefix avoids S3 key hotspots).
    *   Encryption: **SSE-KMS** mandatory. Consider client-side encryption support via SDK for highly sensitive data sources.
    *   Access Control: Bucket policies & IAM restrict access strictly to authorized service roles (e.g., Ingestion API role, Mapping Engine role). Direct user access disallowed. Versioning enabled.
    *   Lifecycle Policies: Define policies for transitioning older raw data to lower-cost storage tiers (e.g., S3 Infrequent Access, Glacier) or eventual deletion based on data retention policies.
*   **Time-Series Data Storage (TimescaleDB on Managed PostgreSQL):**
    *   Schema (`observations` Hypertable - Key Fields): See previous elaboration. Add `metadata` JSONB field for source-specific context.
    *   Partitioning: Automatic time partitioning (e.g., weekly/monthly chunks) via TimescaleDB. Consider composite partitioning including `user_id` or `variable_id` based on query analysis during performance tuning.
    *   Indexes: Primary composite `(user_id, variable_id, timestamp DESC)`. Indexes on `timestamp`, `variable_id`, potentially GIN index on `metadata`.
    *   Data Retention: Configurable via platform settings, potentially tiered (e.g., retain X years in primary hypertable, archive older to S3/cheaper storage, delete after Y years according to consent/policy). Needs robust implementation.
    *   Backup: Leverage managed service provider's automated backups, point-in-time recovery (PITR), and potentially cross-region snapshots for disaster recovery.
*   **Metadata / Relational Storage (PostgreSQL):**
    *   Schema: Maintain detailed ERD and DDL scripts in version control. Enforce referential integrity. Use UUIDs widely. Store hashes of consent documents, not the documents themselves.

### 3.3 Data Mapping & Validation Engine

Handles heterogeneity of input data asynchronously.

*   **Implementation:** Pool of containerized **Python microservices** on EKS, scaling based on SQS queue depth.
*   **Mapping Logic:**
    *   Core Mappers: Prioritize robust implementation for **FHIR (R4/R5 Resources like Patient, Observation, Condition, MedicationRequest, DiagnosticReport), HL7v2 (ADT, ORU, ORM messages via parsing libraries), C-CDA documents, common lab formats (CSV/TSV), and direct API formats from major wearables (Fitbit, Oura, Garmin - requires specific plugins)**. Maintain mapping logic separately from core engine.
    *   Plugin Interface: Defined API for plugins to register custom mappers for specific file types or third-party APIs (see Section 4).
    *   Reference Data Usage: Crucial reliance on `variables` and `units` tables for mapping source terms/units to standardized internal IDs. Handles code system translations (e.g., local lab code to LOINC).
*   **Validation Logic:** Performed *after* mapping to standardized format. Checks against `variables` definitions (range, units). Implements outlier detection algorithms (configurable, e.g., IQR, Z-score) flagging `is_outlier`. Configurable severity levels for validation failures (log, flag, reject).
*   **Error Handling:** Detailed structured logging of errors (input data ref, mapper/validator step, error type). Use of SQS dead-letter queues for persistent failures requiring manual investigation. API endpoint for users/systems to query job status and error details.
*   **Asynchronous Queue (SQS):** Use standard SQS queues. Consider FIFO queues if strict processing order is essential for certain data types, but acknowledge potential throughput limitations.

### 3.4 Data Ownership & Access Control

User-centric control and robust security are paramount.

*   **Authentication:** **AWS Cognito** or self-hosted **Keycloak/Hydra** providing OAuth 2.0/OIDC services. Enforces MFA. Manages user identities and client application registration.
*   **Authorization:** Combination of **RBAC** (defined roles: `data_owner`, `data_custodian` (e.g., parent/guardian), `researcher`, `clinician_delegate`, `app_developer`, `admin`) and **ABAC** enforced via policy engine (e.g., Open Policy Agent integrated at API Gateway/backend) using attributes like user roles, consent scope, data sensitivity level, requested resource category.
*   **Permission/Consent Management:** User-facing interface (part of reference frontend or integrated via API into third-party apps) for viewing data access logs, managing connected applications (OAuth client grants), granting/revoking fine-grained consents (persisted in `consents` table detailing grantee, scope, duration, status). API endpoints provided for these management functions.
*   **Third-Party App Credentials:** Secure storage (e.g., **AWS Secrets Manager** or **HashiCorp Vault**) for user-provided OAuth tokens/API keys needed by connector plugins to access external services (like Fitbit, Oura). Access tightly controlled via IAM roles granted to specific plugin execution environments.
*   **Auditing:** Immutable audit log (e.g., AWS QLDB or append-only table with cryptographic verification) recording all authentication events, authorization decisions, consent changes, data access requests (including denied attempts), and administrative actions.

### 3.5 Reference Data Management

Ensures semantic consistency.

*   **Storage:** Within primary **PostgreSQL** database. Schema detailed previously.
*   **Content:** Actively maintained and expanded. Includes mappings between different coding systems where appropriate (e.g., ICD -> SNOMED). Includes definitions for core dFDA variables not covered by external standards.
*   **Updates & Versioning:** Managed process for updates. Use versioning (e.g., `version` column, valid_from/to dates) on critical definitions (`variables`) to ensure historical data integrity when definitions evolve. API endpoint to retrieve specific versions of definitions.

## 4. Plugin Framework Interfaces

Enables modular extension of platform capabilities.

*   **API Specs (OAS v3.x):**
    *   *Core -> Plugin:* Defined interfaces for triggering specific plugin types (e.g., `POST /plugin/v1/map`, `POST /plugin/v1/analyze`, `GET /plugin/v1/visualize`). Core provides necessary context (data query parameters, user context).
    *   *Plugin -> Core:* Plugins use Core APIs (Ingestion, Data Retrieval, User Management) via standard OAuth tokens. Data Retrieval API (separate spec needed) allows plugins to query user data based on granted consent scope.
*   **Data Formats:** JSON for APIs. Analysis/Visualization plugins receive data in a standardized tabular format (e.g., Pandas DataFrame structure delivered via API response or temporary file access).
*   **Security:** Plugins execute in isolated, containerized environments (e.g., Lambda, specific EKS pods) with least-privilege IAM roles. Core platform rigorously validates plugin requests against user consent *before* executing or providing data access. Network policies restrict plugin communication.
*   **Registration/Discovery:** Plugin Registry stores metadata, including required OAuth scopes, input/output data schemas, and execution endpoints. Core uses this to validate and route requests.

## 5. Security Implementation

Multi-layered security meeting regulatory requirements.

*   **Network Security:** As previously specified (VPC, Security Groups, WAF, Private Subnets).
*   **Application Security:** As previously specified (SAST, DAST, Dependency Scanning, Input Validation, Rate Limiting). Focus on OWASP Top 10.
*   **Data Security:** As previously specified (SSE-KMS, TLS 1.2+, TDE option, Application-level encryption considered for specific PII). Strict IAM policies. Data masking/de-identification capabilities for analytical exports where appropriate.
*   **Authentication & Authorization:** As previously specified (MFA, short-lived tokens, OIDC, RBAC+ABAC).
*   **Compliance:** Explicit controls mapped to **HIPAA** Security Rule (Administrative, Physical, Technical Safeguards) and **GDPR** articles (Lawful Basis, Data Subject Rights, Security of Processing). Regular internal/external audits. BAAs with cloud providers.
*   **Incident Response:** Defined plan, regular testing (tabletop exercises). [Link to Plan]

## 6. Infrastructure & Deployment

Automated, repeatable, and resilient infrastructure.

*   **Infrastructure as Code (IaC):** **Terraform** mandatory for all cloud resources.
*   **CI/CD Pipeline:** **GitLab CI/CD / GitHub Actions** with automated testing (unit, integration, end-to-end), security scans, container builds, and promotion through environments (`dev` -> `staging` -> `prod`). Manual approval gate for production deployments.
*   **Environments:** Isolated AWS accounts or VPCs for `dev`, `staging`, `prod`. Use of realistic (anonymized/synthetic) data in staging for testing.
*   **Scalability Strategy:** As previously specified (Stateless services, HPA, RDS Read Replicas, potential TimescaleDB clustering, ALB).
*   **Disaster Recovery:** As previously specified (Automated backups, cross-region replication strategy, IaC for redeployment, documented DR plan with RPO/RTO targets). Regular DR testing.

## 7. Performance & Scalability Requirements

*(Refined illustrative placeholders)*

*   **Expected Load:**
    *   Users: Target 1M MAU Year 2, 10M MAU Year 4, 100M+ MAU Long-Term.
    *   Data Volume: Ingestion 10 TB/month Year 2, scaling non-linearly. Storage 1 PB Year 4.
    *   API Calls: Peak 5,000 req/sec Year 2.
*   **Latency Requirements:**
    *   Core User-Facing API Read: p95 < 200ms.
    *   Core Data Write (Sync Ack): p95 < 100ms.
    *   Async Ingestion E2E (File Upload -> Queryable): p95 < 5 minutes.
*   **Throughput Requirements:**
    *   Ingestion: Sustain 10,000 observations/sec.
    *   Data Retrieval API: Support 500 concurrent complex analytical queries.
*   **Scalability Targets:** Design to handle 5x current projected peak load; demonstrate horizontal scalability.

## 8. Appendices

*(Placeholders - Content to be generated separately or by human teams)*

*   **Glossary of Technical Terms:** [Link]
*   **Detailed Diagrams:** [Link]
*   **Data Dictionary / Database Schema:** [Link]
*   **API Specifications (OAS Files):** [Link]

---

*This specification is a living document and will be updated as technical decisions are made and implementation progresses.* 