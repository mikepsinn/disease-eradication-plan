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
    *   **Status:** **Core Component.** Required to fulfill mandates in the governing Act (`SEC. 204(c)(4)`, `SEC. 204(i)`).
    *   **Use Cases:** 
        *   **Supply-Chain Integrity:** An immutable ledger, interoperable with DSCSA, for tracking investigational products from manufacturer to patient.
        *   **Privacy-Preserving Audit:** Patient-level transactions (e.g., data access, consent) shall be represented as **zero-knowledge proofs** (e.g., zk-SNARKs) on the ledger, allowing verification without revealing protected health information.
        *   **Consent Management:** Hashing consent forms and permissions to the ledger for an immutable, timestamped record of user intent.
    *   **Implementation:** To be detailed in a separate design document. Will require selection of a suitable L1/L2 protocol, development of smart contracts, and integration with the core platform's API and identity services.
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

### 3.2 Trial Creator Workspace

This section details the backend services required to power the Trial Creator Workspace mandated by the Act.

*   **E-Protocol Builder (`SEC. 204(c)(1)`)**
    *   **Status:** Design Required.
    *   **Description:** A system to allow trial creators to design, validate, and register study protocols.
    *   **Technical Considerations:** Requires dedicated data models for protocol structure (phases, arms, eligibility criteria), a rules engine for automated compliance validation against 21 CFR Parts 312/812 and ISO 14155, and versioning capabilities. Will expose endpoints for creating and managing protocols. To encourage pragmatic and efficient trials, it should also include features like pre-built templates based on the RECOVERY trial, libraries of core outcome sets (COS) for common diseases, and tools to estimate the data collection burden of a given protocol.

*   **Liability-Insurance Exchange (`SEC. 204(c)(2)`)**
    *   **Status:** Design Required.
    *   **Description:** A module to integrate with third-party insurance underwriters to provide real-time quotes for trial liability.
    *   **Technical Considerations:** Requires secure APIs for partner integration, data models for quotes and policies, and integration with the E-Protocol Builder.

*   **Trial Cost, Discount, and Deposit Module (`SEC. 204(c)(3)`)**
    *   **Status:** Design Required.
    *   **Description:** A financial module to manage patient-specific trial costs, application of NIH-funded discounts, and the collection/refund of data provision deposits.
    *   **Technical Considerations:** Requires a secure financial transaction ledger, integration with external payment gateways, and a rules engine for applying discounts. Must be highly auditable.

### 3.3 Trial Execution and Clinical Site Integration

This section outlines the components necessary to execute trials, particularly adaptive and pragmatic trials, and to integrate seamlessly with clinical workflows, as exemplified by the RECOVERY trial.

*   **Adaptive Trial Engine**
    *   **Status:** Design Required.
    *   **Description:** A core service responsible for managing the operational logic of adaptive trials. This is critical for efficiency, allowing trials to change based on interim data.
    *   **Technical Considerations:** Must support various designs (e.g., platform trials, basket trials, response-adaptive randomization). Will include a rules engine to implement protocol-defined adaptation logic (e.g., dropping a treatment arm for futility, adjusting randomization ratios). Requires a secure interface for Data and Safety Monitoring Boards (DSMBs) to review interim analyses.

*   **Clinical Site Integration (eSource/EDC Module)**
    *   **Status:** Design Required.
    *   **Description:** A module to facilitate streamlined data capture directly from clinical sites, minimizing the burden on hospital staff.
    *   **Technical Considerations:**
        *   **EHR Integration:** Must provide robust tools for bi-directional EHR integration (e.g., using HL7 FHIR APIs) to automate the capture of pre-defined clinical outcomes from existing records (eSource).
        *   **Electronic Case Report Forms (eCRF):** Must offer a simple, web-based eCRF interface for clinicians to manually enter the minimal data required by pragmatic protocols, for sites where direct EHR integration is not feasible.
        *   **Workflow Support:** Should integrate with clinical workflows, for example, by providing notifications within the EHR for eligible patients or automating lab test orders required by a protocol.

### 3.4 Data Storage

Layered approach prioritizing raw data integrity and optimized query performance.

*   **Raw Data Storage (AWS S3):**
    *   Bucket Structure: `s3://dfda-raw-data-{env}/{user_id_hash_prefix}/{user_id}/{source_type}/{yyyy}/{mm}/{dd}/{file_uuid}.{ext}` (Hashing prefix avoids S3 key hotspots).
    *   Encryption: **SSE-KMS** mandatory. Consider client-side encryption support via SDK for highly sensitive data sources.
    *   Access Control: Bucket policies & IAM restrict access strictly to authorized service roles (e.g., Ingestion API role, Mapping Engine role). Direct user access disallowed. Versioning enabled.
    *   Lifecycle Policies: Define policies for transitioning older raw data to lower-cost storage tiers (e.g., S3 Infrequent Access, Glacier) or eventual deletion based on data retention policies.
    *   Backup: Leverage managed service provider's automated backups, point-in-time recovery (PITR), and potentially cross-region snapshots for disaster recovery.
*   **Time-Series Data Storage (TimescaleDB on Managed PostgreSQL):**
    *   Schema (`observations` Hypertable - Key Fields): See previous elaboration. Add `metadata` JSONB field for source-specific context.
    *   Partitioning: Automatic time partitioning (e.g., weekly/monthly chunks) via TimescaleDB. Consider composite partitioning including `user_id` or `variable_id` based on query analysis during performance tuning.
    *   Indexes: Primary composite `(user_id, variable_id, timestamp DESC)`. Indexes on `timestamp`, `variable_id`, potentially GIN index on `metadata`.
    *   Data Retention: Configurable via platform settings, potentially tiered (e.g., retain X years in primary hypertable, archive older to S3/cheaper storage, delete after Y years according to consent/policy). Needs robust implementation.
    *   Backup: Leverage managed service provider's automated backups, point-in-time recovery (PITR), and potentially cross-region snapshots for disaster recovery.
*   **Metadata / Relational Storage (PostgreSQL):**
    *   Schema: Maintain detailed ERD and DDL scripts in version control. Enforce referential integrity. Use UUIDs widely. Store hashes of consent documents, not the documents themselves.

### 3.5 Data Mapping & Validation Engine

Handles heterogeneity of input data asynchronously.

*   **Implementation:** Pool of containerized **Python microservices** on EKS, scaling based on SQS queue depth.
*   **Mapping Logic:**
    *   Core Mappers: Prioritize robust implementation for **FHIR (R4/R5 Resources like Patient, Observation, Condition, MedicationRequest, DiagnosticReport), HL7v2 (ADT, ORU, ORM messages via parsing libraries), C-CDA documents, common lab formats (CSV/TSV), and direct API formats from major wearables (Fitbit, Oura, Garmin - requires specific plugins)**. Maintain mapping logic separately from core engine.
    *   Plugin Interface: Defined API for plugins to register custom mappers for specific file types or third-party APIs (see Section 4).
    *   Reference Data Usage: Crucial reliance on `variables` and `units` tables for mapping source terms/units to standardized internal IDs. Handles code system translations (e.g., local lab code to LOINC).
*   **Validation Logic:** Performed *after* mapping to standardized format. Checks against `variables` definitions (range, units). Implements outlier detection algorithms (configurable, e.g., IQR, Z-score) flagging `is_outlier`. Configurable severity levels for validation failures (log, flag, reject).
*   **Error Handling:** Detailed structured logging of errors (input data ref, mapper/validator step, error type). Use of SQS dead-letter queues for persistent failures requiring manual investigation. API endpoint for users/systems to query job status and error details.
*   **Asynchronous Queue (SQS):** Use standard SQS queues. Consider FIFO queues if strict processing order is essential for certain data types, but acknowledge potential throughput limitations.
*   **API Specs (OAS v3.x):**
    *   *Core -> Plugin:* Defined interfaces for triggering specific plugin types (e.g., `POST /plugin/v1/map`, `POST /plugin/v1/analyze`, `GET /plugin/v1/visualize`). Core provides necessary context (data query parameters, user context).
    *   *Plugin -> Core:* Plugins use Core APIs (Ingestion, Data Retrieval, User Management) via standard OAuth tokens. Data Retrieval API (separate spec needed) allows plugins to query user data based on granted consent scope.
*   **Data Formats:** JSON for APIs. Analysis/Visualization plugins receive data in a standardized tabular format (e.g., Pandas DataFrame structure delivered via API response or temporary file access).
*   **Security:** Plugins execute in isolated, containerized environments (e.g., Lambda, specific EKS pods) with least-privilege IAM roles. Core platform rigorously validates plugin requests against user consent *before* executing or providing data access. Network policies restrict plugin communication.
*   **Registration/Discovery:** Plugin Registry stores metadata, including required OAuth scopes, input/output data schemas, and execution endpoints. Core uses this to validate and route requests.

## 4. Plugin Framework Interfaces

Enables modular extension of platform capabilities.

*   **API Specs (OAS v3.x):**
    *   *Core -> Plugin:* Defined interfaces for triggering specific plugin types (e.g., `POST /plugin/v1/map`, `POST /plugin/v1/analyze`, `GET /plugin/v1/visualize`). Core provides necessary context (data query parameters, user context).
    *   *Plugin -> Core:* Plugins use Core APIs (Ingestion, Data Retrieval, User Management) via standard OAuth tokens. Data Retrieval API (separate spec needed) allows plugins to query user data based on granted consent scope.
*   **Data Formats:** JSON for APIs. Analysis/Visualization plugins receive data in a standardized tabular format (e.g., Pandas DataFrame structure delivered via API response or temporary file access).
*   **Security:** Plugins execute in isolated, containerized environments (e.g., Lambda, specific EKS pods) with least-privilege IAM roles. Core platform rigorously validates plugin requests against user consent *before* executing or providing data access. Network policies restrict plugin communication.
*   **Registration/Discovery:** Plugin Registry stores metadata, including required OAuth scopes, input/output data schemas, and execution endpoints. Core uses this to validate and route requests.

## 5. Governance and Automation Systems

This section specifies the systems required to fulfill the unique governance and automation mandates of the Act.

*   **AI-Augmented Governance (`SEC. 204(g)`)**
    *   **Status:** Design Required.
    *   **Description:** An AI-driven system to analyze pull requests to the platform's public source code repository, assign risk scores, and automate the merge/rejection process based on TSC-defined rules.
    *   **Technical Considerations:** Requires integration with repository webhooks (e.g., GitHub Actions), development or integration of a code-analysis AI model, and a rules engine to manage the triage and voting logic for the TSC.

*   **Public Bounty Program (`SEC. 204(i)`)**
    *   **Status:** Design Required.
    *   **Description:** A system to manage the public bounty program for code contributions and vulnerability disclosures.
    *   **Technical Considerations:** Requires integration with repository issue trackers, a payment system, and an automated verification component (potentially leveraging the AI Governance reviewer) to validate submissions and trigger payouts.

## 6. Security Implementation

Multi-layered security meeting regulatory requirements.

*   **Network Security:** As previously specified (VPC, Security Groups, WAF, Private Subnets).
*   **Application Security:** As previously specified (SAST, DAST, Dependency Scanning, Input Validation, Rate Limiting). Focus on OWASP Top 10.
*   **Data Security:** As previously specified (SSE-KMS, TLS 1.2+, TDE option, Application-level encryption considered for specific PII). Strict IAM policies. Data masking/de-identification capabilities for analytical exports where appropriate.
*   **Authentication & Authorization:** As previously specified (MFA, short-lived tokens, OIDC, RBAC+ABAC).
*   **Compliance:** Explicit controls mapped to **HIPAA** Security Rule (Administrative, Physical, Technical Safeguards) and **GDPR** articles (Lawful Basis, Data Subject Rights, Security of Processing). Regular internal/external audits. BAAs with cloud providers.
*   **Incident Response:** Defined plan, regular testing (tabletop exercises). [Link to Plan]

## 7. Infrastructure & Deployment

Automated, repeatable, and resilient infrastructure.

*   **Infrastructure as Code (IaC):** **Terraform** mandatory for all cloud resources.
*   **CI/CD Pipeline:** **GitLab CI/CD / GitHub Actions** with automated testing (unit, integration, end-to-end), security scans, container builds, and promotion through environments (`dev` -> `staging` -> `prod`). Manual approval gate for production deployments.
*   **Environments:** Isolated AWS accounts or VPCs for `dev`, `staging`, `prod`. Use of realistic (anonymized/synthetic) data in staging for testing.
*   **Scalability Strategy:** As previously specified (Stateless services, HPA, RDS Read Replicas, potential TimescaleDB clustering, ALB).
*   **Disaster Recovery:** As previously specified (Automated backups, cross-region replication strategy, IaC for redeployment, documented DR plan with RPO/RTO targets). Regular DR testing.

## 8. Performance & Scalability Requirements

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

## 9. Appendices

*(Placeholders - Content to be generated separately or by human teams)*

*   **Glossary of Technical Terms:** [Link]
*   **Detailed Diagrams:** [Link]
*   **Data Dictionary / Database Schema:** [Link]
*   **API Specifications (OAS Files):** [Link]

---

*This specification is a living document and will be updated as technical decisions are made and implementation progresses.* 