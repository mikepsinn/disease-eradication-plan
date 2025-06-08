# Architectural Diagrams

**Status:** DRAFT
**Version:** 0.1

This directory contains visual diagrams, such as C4 models, sequence diagrams, and infrastructure diagrams, that illustrate the architecture of the platform.

## C4 System Context Diagram

This diagram shows the high-level relationships between the FDA.gov v2 Platform, its users, and the external systems it interacts with.

```mermaid
C4Context
    title System Context diagram for FDA.gov v2 Platform

    Person(patient, "Patient / Trial Participant", "A person using the platform to manage their health data and participate in trials.")
    Person(creator, "Trial Creator / Researcher", "A scientist or institution designing and running a clinical trial.")
    Person(regulator, "Regulator / IRB Member", "An official from the FDA, a peer agency, or an Institutional Review Board (IRB) providing oversight.")
    
    System_Boundary(platform_boundary, "FDA.gov v2 Platform") {
        System(dfda_platform, "FDA.gov v2 Platform", "The core open-source backend (BaaS) for data aggregation, trial management, and evidence generation. Provides APIs, a reference portal, and a public knowledge base.")
    }

    System_Ext(ehr, "EHR / Data Silos", "External Electronic Health Record systems, health apps, and lab systems that are sources of patient data.")
    System_Ext(insurance, "Insurance Underwriters", "Third-party services providing liability insurance for clinical trials.")
    System_Ext(github, "Public Code Repository", "e.g., GitHub. Hosts the open-source code, manages pull requests, and facilitates community contributions.")
    System_Ext(payment, "Payment Gateways", "External services for managing financial transactions for trial participation costs and deposits.")
    System_Ext(national_systems, "National Health Systems", "e.g., NIH All of Us, CDC Surveillance Systems. The platform interoperates with these systems.")

    Rel(patient, dfda_platform, "Contributes data, consents to trials, views findings")
    Rel(creator, dfda_platform, "Designs & manages trials, analyzes results")
    Rel(regulator, dfda_platform, "Monitors trial progress & safety data")

    Rel_L(dfda_platform, ehr, "Pulls data from", "API, FHIR")
    Rel_R(dfda_platform, insurance, "Gets quotes from", "API")
    Rel_R(dfda_platform, github, "Manages source code via", "Git, Webhooks")
    Rel_L(dfda_platform, payment, "Processes payments via", "API")
    Rel_R(dfda_platform, national_systems, "Shares & receives data with", "API, Interoperability Framework")

    UpdateElementStyle(patient, $bgColor="lightgrey", $fontColor="black", $borderColor="black")
    UpdateElementStyle(creator, $bgColor="lightgrey", $fontColor="black", $borderColor="black")
    UpdateElementStyle(regulator, $bgColor="lightgrey", $fontColor="black", $borderColor="black")
    UpdateElementStyle(dfda_platform, $bgColor="blue", $fontColor="white", $borderColor="blue")
```

## Other Diagrams

*   **[Layered Platform Architecture](https://static.crowdsourcingcures.org/img/layered-platform-architecture-diagram.png)**: A high-level view of the core platform and plugin framework.
*   **[Plugin Marketplace](https://static.crowdsourcingcures.org/img/plugin-marketplace.png)**: Illustrates the relationship between the core platform and the third-party plugin ecosystem.

---
*More diagrams will be added here as they are developed.* 