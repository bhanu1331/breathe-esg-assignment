# DECISIONS.md

## Overview
This prototype was designed as a pragmatic ESG data ingestion and analyst review system for enterprise onboarding workflows.

Because the assignment timeline was limited to 4 days, I prioritized building a working end-to-end ingestion + review workflow over implementing every real-world edge case.

The main design principle was:
Build a realistic MVP that demonstrates architectural thinking, auditability, and analyst usability.

---

# 1. Ingestion mechanism choice

## Decision
Used file upload (CSV) ingestion for all three source types.

## Why
Real enterprise ESG workflows frequently involve manual data exports from source systems.

Examples:
- SAP exports are commonly shared as flat files / CSV extracts
- Utility teams often export portal billing data as CSV
- Travel platforms like Concur/Navan support CSV exports

CSV upload allowed a realistic prototype without depending on external APIs or credentials.

## Alternatives considered
- SAP OData integration
- Utility API ingestion
- Concur API integration

## Why not chosen
These require authentication setup, API credentials, rate handling, and significantly more implementation time.

For a prototype, CSV upload demonstrates ingestion logic without unnecessary infrastructure complexity.

---

# 2. SAP data subset

## Decision
Handled SAP fuel/procurement style flat-file export.

## Why
SAP supports many integration mechanisms:
- IDoc
- BAPI
- OData
- Flat file exports

For this prototype, flat file export was chosen because it is common for manual ESG data exchange and easier to validate in an analyst workflow.

## Scope handled
Included:
- fuel quantity
- unit
- source file traceability

Ignored:
- German column variations
- plant code lookups
- procurement category mapping
- date parsing complexity

## Reason
Prototype scope.

---

# 3. Utility ingestion format

## Decision
Handled utility portal CSV export.

## Why
Facilities teams often download CSV usage summaries from electricity provider portals.

CSV provides:
- billing consumption
- units
- usage values

This is realistic for prototype implementation.

## Ignored
Not implemented:
- PDF bill OCR parsing
- tariff breakdown
- billing cycle alignment
- demand charges

## Reason
These would significantly increase complexity.

---

# 4. Travel ingestion format

## Decision
Handled CSV export representing travel platform data.

## Why
Corporate travel platforms commonly support CSV reporting exports.

Handled:
- travel category
- distance
- units

Supported categories:
- flights
- hotel
- ground transport

## Ignored
Not handled:
- airport code route inference
- emission factor differences by cabin class
- hotel room-night normalization

## Reason
Prototype scope prioritization.

---

# 5. Multi-tenancy approach

## Decision
Used tenant-based data isolation.

Each ingestion request includes:

tenant_id

and records are linked to a Tenant model.

## Why
Breathe ESG is enterprise SaaS software.

Different customers must have isolated data.

This prototype demonstrates multi-tenant architecture without implementing full authentication tenancy enforcement.

---

# 6. Normalization model design

## Decision
Separated raw ingestion records from normalized ESG records.

Models:
- DataSource
- RawRecord
- NormalizedRecord

## Why
This preserves:
- source traceability
- auditability
- normalization transparency

This mirrors realistic data pipeline design.

---

# 7. Suspicious data detection

## Decision
Added simple anomaly rules.

Examples:
- unusually high utility consumption
- large SAP fuel values
- zero-distance flights

## Why
Assignment explicitly required:
“what looks suspicious”

This provides a working analyst review mechanism.

## Why simple rules
A rules-based MVP is easier to explain and defend than introducing ML heuristics without validation.

---

# 8. Failed ingestion handling

## Decision
Created FAILED workflow for invalid rows.

If parsing fails:
- row is preserved
- marked FAILED
- visible to analysts

## Why
Assignment required:
“what failed”

Dropping bad rows silently would reduce auditability.

---

# 9. Analyst approval workflow

## Decision
Implemented:
- APPROVE
- REJECT
- LOCK

## Why
Assignment required analyst review before audit lock.

This simulates realistic governance workflow.

Rules:
- pending → approved/rejected
- approved → locked
- locked records immutable

---

# 10. Auditability approach

## Decision
Stored:
- source file
- uploader
- raw payload
- timestamps
- review status
- audit logs

## Why
Audit defensibility is central to ESG reporting workflows.

Analysts and auditors need full traceability.

---

# 11. Authentication scope

## Decision
Used Django admin + prototype endpoints instead of full RBAC auth.

## Why
Assignment focused on ingestion/review architecture rather than production auth.

Full auth would be a production enhancement.

---

# Questions I would ask the PM

1. Which SAP integration path is expected?
CSV, OData, IDoc, or BAPI?

2. Should utility ingestion support PDFs?

3. Should travel emissions be calculated from airport codes when distance is missing?

4. What approval rules should lock records?

5. Are edits allowed after approval?

6. Should tenants be fully isolated by authentication context?

7. What external audit export format is required?