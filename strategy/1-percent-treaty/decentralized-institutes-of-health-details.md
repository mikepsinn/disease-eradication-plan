---
title: The Decentralized Institutes of Health: Revolutionizing Healthcare Through Decentralized Science and AI
description: Exploring the transformative potential of Decentralized Institutes of Health (DIH) in reallocating resources from war to medical breakthroughs using blockchain, AI, and decentralized tools.
published: true
date: 2024-06-09T00:00:00.000Z
tags: decentralized-health, dih, blockchain, ai, medical-research, quadratic-funding, product-requirements
editor: markdown
dateCreated: 2024-06-09T00:00:00.000Z
---

# The Decentralized Institutes of Health

> Note: For the concise overview, see the canonical page: [The Decentralized Institutes of Health](./decentralized-institutes-of-health.md). This page provides extended details and PRD content.

Through decentralized science (DeSci), artificial intelligence (AI),
and leveraging the Gitcoin Grants Stack,
a Decentralized Institutes of Health (DIH)
could facilitate a significant reallocation of resources and human capital from war to the development of medical breakthroughs.

### Organizational Framework

DIH operates through a network of Decentralized Autonomous Organizations (DAOs) dedicated to fostering innovation within specific areas of health and medical research:

- **Research DAOs**: Groups such as VitaDAO and CerebrumDAO would focus on specialized research, employing tokenized models to ensure that public goods and stakeholder-driven development are at the forefront.
- **Technology DAOs & Projects**: With initiatives like Inference Labs and The Bittensor Hub decentralizing the AI stack, DIH could use these tailored AI solutions to propel medical research forward.
- **Patient Advocacy DAOs**: These entities align research and healthcare priorities with patient needs and perspectives.
- **FDAi**: An AI agent designed for everyone that automates, aggregates, and analyzes data, publishes results, offers real-time decision support, and facilitates clinical trial participation across therapeutic areas.

### Expanded Organizational Structure

The DIH is expanding into a comprehensive ecosystem that mirrors the NIH structure while offering decentralized governance, titles, and community-specific focus areas. This expansion serves as a strategic recruitment tool for the 1% Treaty referendum effort.

For the complete organizational structure, including all sub-agencies, earned, criteria-based recognition, and implementation roadmap, see [DIH Organizational Structure](dih-org-structure.md).

### Core Functionalities

DIH approach to healthcare research and development:

- **Programmatic Funding via Gitcoin Grants Stack**: Quadratic funding with sybil-resistant identity, on-chain rules, and automatic disbursement.
- **FDAi Integration**: By automating clinical research processes, the FDAi significantly enhances personalized healthcare, making cutting-edge research and treatment options more accessible.

### Technology

DIH's technological infrastructure would incorporate:

- **Blockchain & AI**: For secure operations and advanced data analysis.
- **Decentralized Data Management**: Facilitating patient recruitment and leveraging composable research elements for a streamlined research process.

### Key Projects and Collaborations

Key components and collaborations within DIH include:

- **BioDAOs & LLMs**: These entities leverage AI and tokenized models for drug development and personalized care.
- **Reputation Systems & DIDs**: Enhancing trust via verifiable credentials and attestations; machine-checked COI disclosures.

### Strategy

The overarching strategy of DIH includes the synergistic operation of AI-powered BioDAOs, DKGs, and Hypercerts,
aiming to create a decentralized, autonomous framework for clinical discovery.

# Product Requirements

Product Requirements Document (PRD)
Decentralized Institutes of Health (DIH) Platform

1. Introduction
   1.1 Purpose
   The purpose of this document is to outline the requirements for the development of the Decentralized Institutes of Health (DIH) platform, a decentralized, democratic, and transparent system for funding and managing medical research projects that prioritize public goods and open access to intellectual property (IP). The platform aims to be a viable alternative to centralized organizations like the National Institutes of Health (NIH) and World Health Organization (WHO).

   1.2 Scope
   The DIH platform will be built using blockchain technology, leveraging the Gitcoin Grants Stack and other decentralized tools to enable quadratic funding, community governance, and public ownership of research outputs. The platform will be accessible to users with varying levels of web3 experience, supporting both fiat and cryptocurrency donations. It will also incorporate features to ensure regulatory compliance, scientific review, IP management, funding diversification, collaboration, data management, education, and monitoring.

2. Functional Requirements
   2.1 User Roles

   - Researchers: Submit project proposals and manage funded projects
   - Funders: Contribute funds to projects and participate in governance
   - Reviewers: Evaluate project proposals and provide feedback

     2.2 Project Submission

   - Researchers can submit project proposals with a description, funding goal, timeline, and regulatory compliance plan
   - Proposals are stored on a decentralized storage solution (e.g., IPFS) and associated with a unique identifier and smart contract

     2.3 Quadratic Funding

   - Funders can contribute to projects using cryptocurrency, stablecoins, or fiat currency
   - Contributions are matched using the quadratic funding formula, with funds allocated from a diversified pool of sources
   - Smart contracts automatically distribute funds to projects based on the funding round results

     2.4 Community Governance

   - Credentialed, timeboxed signaling; on-chain executors apply rules automatically
   - Emergency DAO fallback for narrowly scoped overrides with public justification and automatic sunset
   - Influence derives from verifiable credentials, past performance, and stake where applicable

     2.5 Reputation System

   - Researchers, funders, and reviewers present verifiable credentials and attestations; fraud triggers slashing/blacklisting
   - Credentials influence visibility and eligibility; human discretion minimized

     2.6 Project Management

   - Projects post machine-readable milestones; evidence oracles attest completion; contracts auto-release/claw back funds

     2.7 Intellectual Property Management

   - A flexible IP framework balances open access with the need for limited protection to incentivize innovation
   - The platform provides guidance and support for researchers navigating IP issues and technology transfer processes

     2.8 Scientific Review and Validation

   - A decentralized peer review system uses credential-gated, blinded reviewers selected by algorithm; no standing committees
   - Funding priorities are proposed by AI triage agents with transparent criteria and citations
   - Collaboration with established scientific institutions and journals helps validate and disseminate research findings

     2.9 Funding Diversification

   - The platform seeks partnerships with governments, foundations, and corporations to diversify its funding sources
   - Innovative funding models, such as impact investing and outcome-based financing, are explored

     2.10 Collaboration and Partnerships

   - The platform fosters collaboration among researchers, institutions, and stakeholders to maximize impact
   - Partnerships with healthcare organizations, NGOs, and patient advocacy groups help identify research priorities and disseminate findings

     2.11 Data Management and Sharing

   - Robust data management and sharing protocols ensure the security, privacy, and interoperability of research data
   - Decentralized storage solutions and privacy-preserving technologies are leveraged

     2.12 Education and Outreach

   - The platform invests in education and outreach initiatives to raise awareness about decentralized healthcare research
   - Partnerships with universities and educational institutions help train the next generation of decentralized healthcare researchers

     2.13 Monitoring and Evaluation

   - A comprehensive monitoring framework computes KPIs from on-chain events and data oracles
   - KPIs are defined and tracked via public dashboards and immutable logs
   - Audits are bounty-funded and reproducible; no manual reporting requirements

## How the National Institutes of Health Works

```mermaid
graph TD;
    Congress[U.S. Congress] -->|Allocates Funds| NIH[NIH Administration];
    NIH -->|Distributes Funds| Institutes[Various NIH Institutes];
    NIH -->|Distributes Funds| Centers[NIH Research Centers];
    Institutes --> Grants[Grant Programs];
    Centers --> Contracts[Contracts];
    Grants -->|Application Process| Review[Peer Review Process];
    Contracts -->|Bid/Proposal Review| Review;
    Review -->|Fund Allocation| Recipients[Grant Recipients];
    Recipients -->|Conducts Research| Universities[Universities];
    Recipients -->|Conducts Research| Hospitals[Hospitals];
    Recipients -->|Conducts Research| Industries[Private Industries];
    Universities -->|Research Outcomes| Publications[Publications];
    Hospitals -->|Health Improvements| HealthOut[Improved Health Outcomes];
    Industries -->|Develops Technologies| Tech[New Technologies];
    Publications -->|Feedback| NIH;
    HealthOut -->|Feedback| NIH;
    Tech -->|Feedback| NIH;
    NIH -->|Policy and Funding Decisions| Congress;
    Recipients -->|Direct Benefits| Patients[Patients];
    Patients -->|Feedback| Public[General Public];
    Public -->|Support and Interest| Congress;

```

## How the Decentralized Institutes of Health Would Work

```mermaid
graph TD;
    Congress -->|Allocates Funds| DIH[DIH Administration];
    DIH -->|Distributes Funds| DAOs[Research DAOs];
    DIH -->|Distributes Funds| TechDAOs[Technology DAOs];
    DIH -->|Distributes Funds| PatientDAOs[Patient Advocacy DAOs];
    DIH -->|Distributes Funds| FDAi[FDAi];
    DAOs -->|Funds Projects| Researchers[Researchers];
    TechDAOs -->|Funds Projects| AIProjects[AI Projects];
    PatientDAOs -->|Funds Projects| AdvocacyProjects[Advocacy Projects];
    FDAi -->|Funds Projects| ClinicalTrials[Clinical Trials];
    Researchers -->|Conducts Research| Universities;
    Researchers -->|Conducts Research| Hospitals;
    Researchers -->|Conducts Research| Industries;
    AIProjects -->|Develops AI Solutions| Tech;
    AdvocacyProjects -->|Advocates for Patients| Patients;
    ClinicalTrials -->|Facilitates Trials| Patients;
    Universities -->|Research Outcomes| Publications;
    Hospitals -->|Health Improvements| HealthOut;
    Industries -->|Develops Technologies| Tech;
    Publications -->|Feedback| DIH;
    HealthOut -->|Feedback| DIH;
    Tech -->|Feedback| DIH;
    DIH -->|Policy and Funding Decisions| Congress;
    Researchers -->|Direct Benefits| Patients;
    Patients -->|Feedback| Public;
    Public -->|Support and Interest| Congress;
```

## Decentralized Institutes of Health: Key Components

```mermaid
graph TD
    A[Decentralized Institute of Health] --> B(Gitcoin Grants Stack)
    A --> C(Quadratic Funding Rounds)
    B --> D{Open Source Projects}
    C --> D
    D --> E(Project Submissions)
    E --> |Linked to GitHub Issues| F(Developer Compensation)
    F --> |Upon Completion and Merge| D

    G(Nonprofits) --> |Pool Funds| A
    H(Government Agencies) --> |Pool Funds| A
    I(DAOs) --> |Pool Funds| A

```

3. Non-Functional Requirements
   3.1 Security

   - The platform must be resistant to attacks, hacks, and unauthorized access
   - All transactions and data storage must be encrypted and secure
   - Regular security audits and bug bounties should be conducted

     3.2 Scalability

   - The platform must be able to handle a large number of projects, funders, and transactions
   - The architecture should be designed to scale horizontally as the platform grows
   - Off-chain solutions and layer-2 scaling should be considered for high-volume activities

     3.3 Usability

   - The platform should have a user-friendly interface for all user roles
   - Clear documentation and tutorials should be provided
   - The platform should be accessible to users with varying levels of technical expertise

     3.4 Compatibility

   - The platform should be compatible with popular blockchain networks (e.g., Ethereum, Polygon)
   - Integration with existing decentralized finance (DeFi) and decentralized identity (DID) solutions should be considered
   - The platform should be interoperable with other decentralized science (DeSci) platforms and tools

4. Constraints

   - The platform must be developed using open-source technologies
   - The platform must comply with relevant regulations and legal frameworks
   - The platform must be launched within a specified timeframe and budget

5. Assumptions and Dependencies

   - The platform assumes the availability of sufficient funding and resources for development and maintenance
   - The platform depends on the continued growth and adoption of blockchain and decentralized technologies
   - The platform assumes the willingness of researchers, funders, and stakeholders to participate in a decentralized model

6. Glossary

   - DAO: Decentralized Autonomous Organization
   - DeSci: Decentralized Science
   - DID: Decentralized Identity
   - IPFS: InterPlanetary File System
   - IP: Intellectual Property
   - PRD: Product Requirements Document

7. References
   - Gitcoin Grants Stack: https://gitcoin.co/grants/
   - Gitcoin Passport: https://passport.gitcoin.co/
   - Quadratic Funding: https://wtfisqf.com/
   - Decentralized Science (DeSci): https://desci.pub/
   - Fortmatic: https://fortmatic.com/
   - Torus: https://tor.us/
