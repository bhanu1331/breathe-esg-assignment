# DECISIONS.md

## Overview
This document explains architectural and implementation decisions made during the prototype build, including tradeoffs and assumptions due to assignment constraints.

---

## 1. Ingestion mechanism choice

### Decision
Used file upload ingestion for all three source types.

### Why
The assignment allowed choosing ingestion mechanisms.

Given a 4-day prototype constraint, file upload provided:
- faster implementation
- reproducible testing
- deterministic sample inputs
- easier analyst simulation

It also reflects realistic operational workflows where enterprise teams often export data manually for ESG reporting.

---

## 2. SAP source format choice

### Decision
Modeled SAP as flat-file CSV export.

### Why
SAP integrations can involve:
- IDoc
- OData
- BAPI
- flat exports

For a prototype, flat export was chosen because many finance/procurement teams still export SAP data to CSV or Excel for reconciliation workflows.

CSV ingestion also reduced authentication and SAP environment dependency.

### Subset handled
Handled:
- fuel/procurement-style quantity records
- plant code
- material description
- posting date
- vendor

### Ignored
Not handled:
- SAP authentication
- IDoc parsing
- multilingual column mapping
- plant code lookup tables
- procurement category complexity

### PM question
Would the client prefer:
- direct SAP integration
or
- batch file ingestion?

---

## 3. Utility source choice

### Decision
Modeled utility ingestion as CSV export from utility portal.

### Why
Facilities teams commonly export billing/consumption data from web portals.

Compared to PDF parsing:
CSV is:
- more structured
- less error-prone
- faster to prototype

PDF parsing would require OCR and layout handling beyond prototype scope.

### Subset handled
Handled:
- meter identifier
- billing period
- consumption
- unit
- tariff type

### Ignored
Not handled:
- PDF bill parsing
- utility APIs
- multi-meter aggregation
- tariff cost modeling
- month alignment logic

### PM question
Will customers primarily provide:
- CSV exports
- PDFs
- API credentials?

---

## 4. Travel source choice

### Decision
Modeled travel ingestion as CSV export.

### Why
Corporate travel platforms like Concur or Navan expose structured travel records.

For prototype simplicity, CSV export was used to represent:
- flights
- hotels
- ground transport

This simulates analyst-import workflows.

### Subset handled
Handled:
- trip category
- origin
- destination
- distance
- distance unit

### Ignored
Not handled:
- airport code distance resolution
- hotel emissions factors
- API authentication
- itinerary segmentation

### PM question
Should travel ingestion be:
- API-based
- batch upload
- both?

---

## 5. Database choice

### Decision
Used SQLite.

### Why
Fastest prototype database for local development.

Reduces infrastructure complexity.

Production systems would use PostgreSQL.

---

## 6. Django REST choice

### Decision
Used Django REST Framework.

### Why
Assignment explicitly requested Django REST.

Benefits:
- rapid API creation
- serializer support
- admin interface
- ORM-backed data model

---

## 7. React frontend choice

### Decision
Used React dashboard.

### Why
Assignment explicitly required React.

React provides:
- responsive UI
- API integration
- analyst interaction workflows

---

## 8. Suspicious record logic

### Decision
Implemented rule-based anomaly checks.

Rules:
- fuel > 10000
- electricity > 50000
- flight distance = 0

### Why
Prototype needed suspicious review functionality.

Simple deterministic rules demonstrate analyst escalation flow.

### PM question
Should suspicious detection use:
- business thresholds
- ML anomaly detection
- configurable tenant rules?

---

## 9. Failed ingestion handling

### Decision
Bad rows are converted into FAILED normalized records instead of crashing ingestion.

### Why
Assignment required analysts to see failed records.

This improves reliability and audit visibility.

---

## 10. Audit locking

### Decision
Added LOCKED status.

### Why
Assignment explicitly states:
approve rows before they are locked for audit.

Locked records reject further changes.

---

## 11. Multi-tenancy

### Decision
Tenant isolation enforced through foreign keys.

### Why
Breathe ESG serves multiple enterprise customers.

Prototype must avoid tenant data mixing.

---

## Design summary

This prototype prioritizes:
- auditability
- explainability
- realistic enterprise workflows
- fast prototype delivery