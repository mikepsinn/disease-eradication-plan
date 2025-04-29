# Help DOGE Improve Regulations to Accelerate BioMedical Innovation

### First Name

### Last Name

### Email

### What is the rule, regulation (federal register entry), or agency guidance document (not statutes, sorry!) you'd like modified or rescinded?

HIPAA Privacy Rule (45 CFR Parts 160, 164) & related Guidance

### What is the respective Federal register entry? (if an agency guidance document, write that)

45 CFR Parts 160 and 164; Various HHS/OCR Guidance Documents on HIPAA

### Tell me what the rule, regulation or guidance document is supposed to do (be generous to it)

The HIPAA Privacy Rule establishes national standards to protect individuals' medical records and other identifiable health information (Protected Health Information - PHI). It sets limits and conditions on the uses and disclosures that may be made of such information without patient authorization, and gives patients rights over their health information, including rights to examine and obtain a copy of their health records and to request corrections.

### Tell me what it actually does (i.e. what are the its impact, intentional or unintentional - details and numbers are helpful here even if estimates). If both good and bad impacts exist, address both.

While providing essential privacy protections, HIPAA's implementation and interpretation can create significant challenges for large-scale data aggregation, research, and platform operations like dFDA:
*   **Complexity for Large-Scale Data:** Applying HIPAA rules to the aggregation and analysis of RWD from diverse sources via a central platform can be complex, requiring careful structuring of data use agreements and technical safeguards.
*   **De-identification Challenges:** Standards for de-identification (e.g., Safe Harbor, Expert Determination) can be difficult and costly to apply consistently to large, complex, longitudinal datasets common in RWE, potentially limiting data utility.
*   **Patient Data Control Ambiguity:** While patients have rights, the practical mechanisms for exercising granular control over data use (especially for secondary research) and revoking consent/permissions within large, complex platforms are often unclear or poorly implemented.
*   **Barriers to Data Sharing/Linkage:** Perceived HIPAA risks or ambiguities can create barriers for healthcare providers and other entities sharing data with research platforms, even for legitimate research purposes.
*   **Restrictions on Secondary Use:** Interpretations can unduly restrict valuable secondary research use of data, even when appropriate privacy safeguards (like robust anonymization or aggregation) are in place.
*   **Lack of Explicit Data Ownership:** HIPAA focuses on privacy/security of PHI held by covered entities, but doesn't explicitly establish individual *ownership* of raw health data.

### Should it be rescinded, and if so, why? (remember, if something has some good impact, it may be hard to rescind without a replacement, so modifying may be the better course)

No. Foundational privacy protections are crucial for public trust and participation. However, guidance and interpretations should be significantly updated to clarify requirements for modern data platforms, facilitate research, and empower patients, and some interpretations hindering data use should be repealed.

### Should it be modified and if so, how?

Yes, guidance and interpretations should be modified/clarified:
*   **Platform-Specific HIPAA Guidance:** Issue specific guidance from HHS/OCR on HIPAA compliance tailored for dFDA-like platforms, addressing data use agreements, appropriate use of secure multi-party computation/federated learning, robust de-identification/anonymization techniques for large datasets, and secure data aggregation practices.
*   **Clarify Patient Control:** Issue guidance clarifying standards for implementing granular, patient-controlled permissions for data use (primary trial, secondary research, commercial use, etc.) and revocation mechanisms within the platform context, potentially recognizing blockchain for immutable consent/permission logging.
*   **Explicitly Recognize Patient Ownership:** Issue guidance interpreting HIPAA and related principles to maximize patient control and portability, **explicitly recognizing the principle of individual ownership of raw health data** contributed to platforms.
*   **Facilitate Secondary Research:** Modify guidance to explicitly facilitate broad **opt-out** consent models for secondary research use of appropriately anonymized/aggregated dFDA data, managed via the platform. Repeal interpretations hindering secondary use when robust, patient-controlled privacy mechanisms are in place.
*   **Facilitate Third-Party Ratings:** Explicitly state in guidance that HIPAA **does not prohibit** and should **facilitate** architectures enabling the creation of third-party safety/efficacy rating systems using appropriately anonymized/aggregated dFDA data. Repeal interpretations hindering responsible data flow for these purposes.
*   **Data Sharing Safe Harbors:** Explore safe harbors or clearer guidance to reduce perceived risks for entities sharing data with certified, secure research platforms like dFDA for legitimate research purposes under appropriate data use agreements. 