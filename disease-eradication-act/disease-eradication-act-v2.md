# Right‑to‑Trial and FDA Upgrade Act of 2025

**Be it enacted by the Senate and House of Representatives of the United States of America in Congress assembled,**

---

## TITLE I — SHORT TITLE; FINDINGS; DEFINITIONS

### SEC. 101. SHORT TITLE.

This Act may be cited as the **“Right‑to‑Trial and FDA Upgrade Act of 2025.”**

### SEC. 102. FINDINGS.

Congress finds the following:

1. Less than **10 percent** of U.S. patients enroll in interventional clinical trials;\[1] distance, eligibility restrictions, and direct costs are principal barriers.
2. Median per‑patient cost for a phase‑3 drug trial in 2024 exceeded **\$43 000**\[2], inflating drug prices and limiting R‑&‑D on unpatentable therapies.
3. The U.K. **RECOVERY** pragmatic trial enrolled 49 000 patients in 100 days at roughly **\$500 per patient**\[3], demonstrating 90 percent cost reduction via adaptive, decentralized design.
4. Publicly financed, algorithm‑targeted subsidies that maximize **quality‑adjusted life‑years (QALYs) per federal dollar** can democratize access while a modest patient co‑payment curbs moral hazard.
5. A single, open‑source **FDA v2 Digital Platform**—with e‑protocol builders, liability‑insurance bidding, blockchain custody, and AI‑ranked treatment lists—will enable any willing patient to join a trial of the most‑promising therapy for their condition.
6. Modernizing FDA regulation to embrace real‑world evidence, remote monitoring, and validated non‑animal test methods will accelerate safe cures.

### SEC. 103. DEFINITIONS.

In this Act—

1. **Secretary** means the Secretary of Health and Human Services.
2. **FDA** means the Food and Drug Administration.
3. **NIH** means the National Institutes of Health.
4. **Pragmatic decentralized trial** means a clinical study integrated into routine care, allowing remote or local data capture, minimal exclusions, and broad patient demographics.
5. **Most‑promising treatment** means an intervention that—(A) ranks within the top decile of projected QALY gain for a condition under SEC. 204(g)(3) or (B) holds Breakthrough Therapy or RMAT designation under section 506 of the Federal Food, Drug, and Cosmetic Act.
6. **QALY** means a quality‑adjusted life‑year, one year of life in perfect health.

---

## TITLE II — FDA Upgrade AND CLINICAL‑TRIAL INNOVATION

### SEC. 201. ACCELERATED ADOPTION OF ALTERNATIVE PRECLINICAL TEST METHODS.

(a) **Rulemaking.** Not later than 180 days after enactment, the Secretary, acting through the Commissioner of Food and Drugs, shall issue final regulations amending 21 C.F.R. Parts 312 and 600 to permit non‑animal New‑Approach Methodologies (NAMs)—including organ‑on‑chip systems, validated in‑silico toxicology, and high‑throughput cell assays—as acceptable primary evidence of safety where scientifically justified.
(b) **Qualification pathway.** The regulations shall establish a transparent qualification pathway; once a NAM is qualified for a defined context of use, FDA reviewers shall accept data from that method without requiring parallel animal studies.
(c) **Annual report.** The Commissioner shall publish an annual public report enumerating qualified NAMs, sponsor submissions using NAMs, and areas still requiring animal use with timelines to develop alternatives.

### SEC. 202. GUIDANCE ON DECENTRALISED, ADAPTIVE, AND REAL‑WORLD‑EVIDENCE TRIALS.

(a) **Decentralised Trials Guidance.** Within 1 year the Secretary shall issue final guidance recognising remote visits, tele‑investigator oversight, direct‑to‑patient IMP shipment, and e‑consent—as compliant with 21 C.F.R. Parts 50, 54, and 312.
(b) **Adaptive Designs.** Guidance shall allow response‑adaptive randomisation, Bayesian interim analyses, seamless phase 2/3 designs, and platform/master‑protocol structures, provided pre‑specified statistical control of type‑I error.
(c) **Real‑World Evidence.** Within 18 months the Secretary shall publish a framework specifying how real‑world data (EHRs, claims, device feeds) integrated via the FDA v2 Platform may support new indications, post‑marketing commitments, or safety label changes.
(d) **Training.** FDA shall establish continuing‑education modules to train reviewers in decentralized‑trial oversight, Bayesian statistics, and RWE analytics.

### SEC. 203. PATIENT‑FOCUSED DRUG DEVELOPMENT AND GLOBAL COLLABORATION.

(a) **Patient Experience Integration.**  FDA shall revise Patient‑Focused Drug Development guidance to require that every pivotal trial protocol include at least one patient‑reported outcome or patient‑preference study relevant to benefit–risk assessment.
(b) **Global Work‑sharing.** The Secretary may enter into work‑sharing arrangements with peer regulators (EMA, PMDA, Health Canada) for concurrent review of applications utilising FDA v2 Platform data.
(c) **Data Standards Convergence.** The Secretary shall align FDA data standards with HL7 FHIR Release 5, CDISC SDTM v4, and SNOMED‑CT 2025 edition to ensure cross‑border data utility.

### SEC. 204. FDA V2 DIGITAL PLATFORM.

(a) **Launch & Hosting.** Within 12 months after enactment the Secretary shall deploy an open‑source, cloud‑native **FDA v2 Digital Platform**\[4] at a publicly accessible sub‑domain of *fda.gov* (e.g., **trials.fda.gov**).  All non‑classified source code shall be mirrored in real‑time to a public repository (e.g., *github.com/fda/fda‑v2*).
(b) **Mandatory Open‑Source Licence.** Except for cybersecurity modules whose disclosure would create a material national‑security risk, all code shall be released under the Apache 2.0 or MIT licence.  Any proprietary dependency shall be replaced or dual‑licensed within 24 months.
(c) **Sponsor Workspace Functions.** The Platform shall provide—
  (1) **E‑Protocol Builder** with automated compliance validation (21 C.F.R. Parts 312/812, ISO 14155).
  (2) **Liability‑Insurance Exchange** for real‑time per‑subject quotes; selections auto‑populate FDA Form 1572.
  (3) **Pricing & Deposit Module** supporting refundable deposits or participant incentives that, in aggregate, do \*\*not exceed USD 500 per participant in any 12‑month period, \*\*indexed annually to the Consumer Price Index for All Urban Consumers (CPI‑U)\*\*\*\*; all such payments shall comply with the Anti‑Kickback Statute safe‑harbour at 42 C.F.R. § 1001.952(bb)\[7] and be transparently disclosed to participants during e‑consent.).
  (4) **Blockchain Supply‑Chain Ledger\[9]** interoperable with DSCSA (§ 360eee‑3) to capture temperature, custody, delivery.
  (5) **Live Analytics Dashboards** for enrolment, compliance, blinded efficacy; regulators & IRBs get read‑only oversight.
(d) **Patient Portal Functions.** The Platform shall—
  (1) Provide symptom/diagnosis intake and a continuously updated **ranked list of treatments & trials**.
  (2) Permit single‑session e‑screening, Part 11 e‑consent, instant randomisation.
  (3) Coordinate direct‑to‑patient or local‑pharmacy IMP dispatch with ledger verification.
  (4) Capture outcomes via mobile app, SMS/IVR, FHIR push, and IoT feeds; data loop into evidence rankings which are **recomputed nightly**.  **The source code, feature weights, and a reproducible computational notebook for each annual release of the QALY‑ranking algorithm shall be posted in the public repository within 30 days of model deployment.**
(e) **Open API & Interoperability.** All de‑identified data shall be exposed through a RESTful API that is HL7 FHIR‑R5 compliant and meets 42 U.S.C. § 300jj‑52.  Third‑party apps may integrate via OAuth 2.0 consent.
(f) **Continuous Integration/Continuous Deployment (CI/CD).** The Secretary shall maintain automated unit‑test, security‑scan, and code‑quality pipelines that must pass before any code merge.  CI results shall be publicly viewable and the Platform shall maintain compliance with **FedRAMP‑Moderate\[6]** and **NIST SP 800‑218** DevSecOps guidelines; the System Security Plan and Authority‑to‑Operate letter shall be posted in redacted form.
(g) **Governance & Pull‑Request Acceptance.** 
  (1) **Technical Steering Committee (TSC).** A nine‑member TSC is hereby established to steward the repository.  Composition: 3 FDA officials, 1 NIH representative, 1 patient‑advocacy representative, 1 open‑source community member elected by contributors, 1 biostatistician, 1 cyber‑security expert, and 1 industry sponsor representative.
  (2) **Decision Process.** The TSC shall operate under an open‑governance model (e.g., Linux Foundation rules of procedure).  Pull requests (PRs) that: (A) pass all CI tests; (B) adhere to published coding standards; and (C) implement bug‑fixes, security patches, or features consistent with statutory requirements **shall be merged within 30 calendar days** unless two‑thirds of the TSC votes to reject and publishes a written rationale.
  (3) **Appeal.** Any contributor may appeal a rejection to the FDA Chief Scientist, who must respond within 30 days.  If the appeal is upheld, the PR is merged automatically.
  (4) **Democratic Renewal.** Community‑elected and patient‑advocate seats are subject to annual election by contributors (defined as those with ≥10 merged PRs in the preceding year) using ranked‑choice voting via a transparent, verifiable online ballot.
(h) **Rulemaking & PRA Fast‑Track.** Within 180 days the Secretary shall issue interim final rules specifying technical standards for each module, codifying the TSC charter, and **invoking 44 U.S.C. § 3507(h) such that any Information‑Collection Request\[5] tied to the FDA v2 Platform obtains OMB clearance within 60 days**.  Sponsors or investigators that fail to comply with these rules may be suspended under 21 U.S.C. § 331(f).

(i) **Public‑Bounty & Zero‑Knowledge Ledger.** The Secretary shall operate a continuous public bounty program—funded under § 402(a)—to reward external contributors for merged pull‑requests, vulnerability disclosures, and feature enhancements.  Bounties shall be posted openly as issues in the public repository with dollar amounts and paid within 30 days of merge.  Furthermore, **all patient‑level transactions logged to the Blockchain Supply‑Chain Ledger shall be represented as zero‑knowledge proofs (e.g., zk‑SNARK commitments) and stored via content‑addressable storage, permitting any nation‑state or regional authority to run an independent mirror node and verify ledger integrity without accessing protected health information.**

(j) **Metrics & Transparency.** Annual public report: platform uptime, median time‑to‑trial launch, pull‑request merge rate, unresolved PR backlog, bounty payouts, penetration‑test findings, insurance‑premium benchmarks, and user‑satisfaction scores.  The Secretary shall commission an independent **penetration test** every fiscal year and publish an executive summary of findings.
(i) **Metrics & Transparency.** Annual public report: platform uptime, median time‑to‑trial launch, pull‑request merge rate, unresolved PR backlog, insurance‑premium benchmarks, user‑satisfaction scores.

## TITLE III — UNIVERSAL TRIAL ACCESS (RIGHT‑TO‑TRIAL PROGRAM)

### SEC. 301. UNIVERSAL ELIGIBILITY FOR INVESTIGATIONAL INTERVENTIONS.

(a) **Right.** Beginning 24 months after enactment, any U.S. resident with a qualifying condition who requests an investigational intervention **shall be guaranteed enrolment—remotely if necessary—in at least one pragmatic, decentralized trial arm evaluating that intervention**, provided the patient meets minimal safety criteria in subsection (c).

(b) **Sponsor Incentive.** The Secretary shall award a **transferable Priority‑Review Voucher (PRV)** under section 524A of the Federal Food, Drug, and Cosmetic Act to any sponsor that, on or before the universal‑enrolment activation date, opens or amends a trial on the FDA v2 Platform to accept such patient‑directed enrolment and maintains adequate investigational‑product supply.  A PRV is forfeited if the sponsor later restricts patient enrolment without a documented safety or manufacturing constraint.

(c) **Safety‑Based Exclusions Only.** Sponsors or IRBs may exclude an individual patient **solely for documented, evidence‑based safety reasons** (e.g., a specific contraindication, allergy, or organ‑system risk) or if investigational‑product supply is demonstrably insufficient.  Exclusion rationales must be transmitted to the FDA Dashboard within 7 days and are subject to FDA audit.

(d) **NIH Micro‑Study Fallback.** If no sponsor operates an active investigational‑new‑drug application that can accept the patient within 60 days of request, the NIH—using Other Transaction Authority—shall initiate a single‑arm or adaptive micro‑study to provide the intervention under IND and collect outcomes via the Platform; such micro‑studies qualify for subsidies under § 303.

(e) **Adaptive Enrolment.** Sponsors participating under this section must accept data‑driven lowering of exclusion criteria unless an IRB documents incremental safety risk.

### SEC. 302. PATIENT PROTECTIONS, CONSENT, AND LIABILITY. PATIENT PROTECTIONS, CONSENT, AND LIABILITY.

(a) **Central IRB.** All Right‑to‑Trial protocols shall undergo single‑IRB review per 45 C.F.R. § 46.114\[8]; FDA shall publish a master reliance agreement.
(b) **Informed Consent.** Platform e‑consent shall disclose investigational nature, known/unknown risks, mandatory patient co‑pay (SEC. 304), and data‑sharing terms; execution of the e‑consent **constitutes both 45 C.F.R. § 164.508 authorization and, where applicable, a waiver of authorization under § 164.512(i)\[11] for research use of protected health information**, as approved by the reviewing IRB; signed consent is hashed and stored on the blockchain ledger.
(c) **Safety Monitoring.** Sponsors must stream adverse‑event data to the Dashboard within 24 hours; FDA may halt enrolment under 21 C.F.R. § 312.42.
(d) **Liability Shield.** Good‑faith compliance grants immunity from tort claims except for gross negligence or willful misconduct; mirrors Pub. L. 115‑176 § 2(c).

### SEC. 303. NIH PARTICIPATION SUBSIDIES.

(a) **Fund.** A revolving Clinical‑Trial Participation Subsidy Fund is established; authorized to receive \$2 billion FY 2026–30.
(b) **Allocation Algorithm.** NIH shall publish an open optimisation model maximising QALYs per dollar and marginal scientific value; algorithm recomputed annually.
(c) **Payments.** NIH pays sponsors per enrolled participant up to the algorithmic cap; sponsors certify costs and submit outcomes.
(d) **Audit.** GAO shall audit fund disbursements biennially; claw‑back for mis‑certified costs.

### SEC. 304. PATIENT COST‑SHARING.

(a) **Minimum Co‑payment. Each participant shall pay a non‑zero fee set by the Secretary between the 25th and 75th percentile of commercial‑insurance specialist‑visit copays for the preceding year, **adjusted annually by the CPI‑U** (initially \$15–\$40 per visit).** Each participant shall pay a non‑zero fee set by the Secretary between the 25th and 75th percentile of commercial‑insurance specialist‑visit copays for the preceding year (initially \$15–\$40 per visit).
(b) **Cap.** Sponsors may not bill participants beyond the statutory co‑pay; NIH subsidy + sponsor absorb remaining costs.
(c) **Disclosure.** Cost schedule and co‑pay displayed in e‑consent; participants may terminate if costs subsequently rise.

---

## TITLE IV — GENERAL PROVISIONS

### SEC. 401. COORDINATION WITH EXISTING LAW.

(a) **Expanded Access.** This Act supplements 21 C.F.R. § 312 Subpart I; data from Right‑to‑Trial may fulfill post‑marketing study obligations.
(b) **State Laws.** No State or political subdivision may regulate the practice of tele‑medicine, pharmacy licensure, or shipment of investigational products in a manner that prevents implementation of this Act.  Specifically, a licensed prescriber participating under an FDA‑approved protocol shall be deemed licensed in all States for the limited purpose of providing investigational treatment under this Act, and pharmacies dispensing or shipping such products pursuant to the blockchain supply‑chain ledger are exempt from conflicting State prohibitions.
(c) **AKS Safe Harbour.** Payments or deposits authorised under SEC. 204(b)(3) are deemed protected remuneration under 42 C.F.R. § 1001.952(bb).
(d) **DSCSA Alignment.** All investigational shipments must utilize the platform ledger to satisfy DSCSA traceability.

### SEC. 402. AUTHORIZATION OF APPROPRIATIONS AND STAGE‑GATED FUNDING.

(a) **FDA Upgrade.** \$500 million FY 2026‑30, of which **no more than 25 percent may be obligated** until the Platform (1) attains FedRAMP‑Moderate ATO *and* (2) records at least **1 000 merged pull‑requests** under § 204(g).  Subsequent 25‑percent tranches unlock upon the Platform reaching 10 000 users and 10 000 merged pull‑requests, respectively.
(b) **Subsidy Fund.** \$2 billion FY 2026‑30, released quarterly upon NIH certification that the subsidy‑allocation algorithm achieved or exceeded its projected QALY gain in the preceding quarter.
(c) **Regulatory‑Science Grants.** \$150 million FY 2026‑30.
(d) **Direct‑Hire Authority.** For FY 2026‑30 the Secretary may hire up to **200 technical employees** for the Platform under 5 U.S.C. § 9803 (critical‑need direct hire).
(e) **Agile Acquisition Pilot.** All contracts for the Platform are designated “modular IT acquisitions” under FITARA; FAR Part 15 documentation requirements are waived in favour of the **US Digital Service Playbook\[10]** incremental‑delivery model.\*\* \$150 million FY 2026‑30.

### SEC. 403. IMPLEMENTATION TIMELINE.

* **180 days:** Interim rules; beta e‑protocol builder; transparency website live.
* **12 months:** FDA v2 Platform MVP; insurance exchange; blockchain ledger operational.
* **24 months:** Universal enrolment guarantee active; subsidies flowing.
* **36 months:** First GAO report to Congress.

### SEC. 404. SEVERABILITY.

If any provision of this Act is held invalid, the remainder shall remain in effect.

---

### REFERENCES

\[1] ClinicalTrials.gov FY 2024 Annual Report, Table 4 (trial enrollment).
\[2] FDA/CDER *Estimating the Cost of Phase‑3 Trials* (2024), Table 3.
\[3] RECOVERY Collaborative Group, “Cost‑efficient Platform Design,” *Health Technology Assessment Meeting*, 2022.
\[4] openFDA GitHub Repository, [https://github.com/FDA](https://github.com/FDA).
\[5] 44 U.S.C. § 3507(h) fast‑track provision; Administrative Conference PRA Study (2012).
\[6] FedRAMP FAQ, ‘Understanding Baselines & Impact Levels’ (2024).
\[7] 42 C.F.R. § 1001.952(bb) (value‑based safe‑harbour).
\[8] 45 C.F.R. § 46.114, NIH Single‑IRB Policy (updated 2023).
\[9] FDA *DSCSA Pilot Project Program – Final Report* (2024).
\[10] U.S. Digital Service, *Digital Service Playbook* (2025).
\[11] 45 C.F.R. § 164.512(i)(1) (HIPAA research waiver).

**End of Act.**
