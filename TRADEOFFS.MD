# TRADEOFFS.md

## Overview
This prototype was intentionally scoped for a 4-day engineering assignment. Several production-grade capabilities were deliberately not built in order to prioritize core ingestion, normalization, analyst review, and audit workflows.

---

## 1. Real external integrations were not implemented

### Not built
Direct integrations with:
- SAP OData / BAPI / IDoc
- utility provider APIs
- Concur / Navan APIs

### Why
These integrations require:
- authentication handling
- credentials management
- vendor-specific schemas
- API rate limits
- environment setup

This would significantly increase complexity and reduce focus on the core ESG ingestion workflow.

### Prototype alternative
Used realistic file-based ingestion representing exported operational data.

### Real production implementation
Production would likely support:
- scheduled API pulls
- webhook ingestion
- credential vault integration
- ingestion retry pipelines

---

## 2. Emissions calculation engine was not implemented

### Not built
Actual carbon emissions calculations.

Examples:
- fuel → CO2e conversion
- electricity region-based emissions factors
- flight emissions estimation

### Why
The assignment explicitly emphasized:

> the hard part is ingesting and normalizing messy enterprise data

This prototype focused on ingestion architecture and analyst workflow rather than emissions math.

### Prototype alternative
Focused on normalized operational activity records.

### Real production implementation
Would integrate:
- emissions factor databases
- geography-aware calculations
- methodology versioning
- audit-grade factor traceability

---

## 3. Advanced data normalization was intentionally simplified

### Not built
Complex unit conversion and schema reconciliation.

Examples:
- gallons → liters
- MWh → kWh
- miles → km
- multilingual SAP headers
- plant code lookup resolution

### Why
Prototype goal was workflow demonstration, not full enterprise normalization coverage.

Implementing every real-world edge case would reduce delivery speed and clarity.

### Prototype alternative
Standardized a narrow but representative subset:
- liters
- kWh
- km

### Real production implementation
Would include:
- configurable mapping rules
- lookup tables
- tenant-specific transformations
- schema versioning

---

## Additional intentionally deferred items

Also deferred:
- authentication / RBAC
- analyst user accounts
- background job processing
- async ingestion
- file storage service integration
- PDF OCR parsing
- duplicate detection
- row editing UI
- bulk approve actions
- retry workflows
- alerting / notifications

---

## Tradeoff philosophy

The assignment emphasized judgment over feature volume.

This prototype intentionally prioritized:
- realistic ingestion workflows
- audit traceability
- analyst review lifecycle
- explainable design decisions

instead of overbuilding partially complete production features.