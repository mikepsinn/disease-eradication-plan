---
title: Organizational Structure
description: Defines the organizational charts for the for-profit management company (SPV) and the non-profit foundation that comprise the initiative.
published: true
date: '2025-08-15T00:00:00.000Z'
tags: [org-chart, strategy, legal, hiring, governance]
editor: markdown
dateCreated: '2025-08-15T00:00:00.000Z'
topic_id: organizational-structure
canonical: true
status: active
domains: [cross]
doc_type: ops
---

# Organizational Structure

This document outlines the organizational structure of the two core entities that drive the War on Disease initiative: the For-Profit Management Company (SPV) and the Non-Profit Foundation.

This structure is designed to separate the operational execution and fundraising activities from the mission oversight and governance, ensuring both efficiency and integrity.

See [Pre-Seed Strategy](../strategy/pre-seed-strategy.md) for details on the roles and responsibilities of the initial hires.

## 1. For-Profit Management Company (SPV)

This entity is the operational engine. It employs the core team, raises investment capital, and executes the strategy.

```mermaid
graph TD;
    subgraph "For-Profit Management Co. (SPV)"
        A["Board of Directors<br/>(Investors & Founder)"];
        B["Managing Director"];
        
        C["Capital Markets Lead"];
        D["Elections & IE Compliance Lead"];
        E["Growth & Referrals Lead"];
        
        F["<br><br>Future Hires<br>(Post-Seed Round)<br>Engineering Lead, Design Lead, etc."];

        A --> B;
        B --> C;
        B --> D;
        B --> E;
        B -.-> F;
    end
    
    style F fill:#fff,stroke:#ccc,stroke-dasharray: 5 5
```

## 2. Non-Profit Foundation

This entity is the guardian of the mission. It provides legal and ethical oversight to ensure the project remains aligned with its public benefit goals.

```mermaid
graph TD;
    subgraph "Non-Profit Foundation"
        A["Board of Trustees<br/>(Independent, Mission-Aligned)"];
        B["(Future) Executive Director"];
        A --> B;
    end

    subgraph "For-Profit Management Co. (SPV)"
        C["Founder & Managing Director"];
    end

    A -- "Provides Mission<br/>Oversight To" --> C;
```
