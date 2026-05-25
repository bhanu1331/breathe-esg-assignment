# MODEL.md

## Overview
This prototype is designed to ingest ESG-related operational data from multiple enterprise sources, normalize it into a common schema, and support analyst review before audit sign-off.

The design prioritizes:
- multi-tenancy
- source traceability
- auditability
- normalized ESG categorization
- analyst review workflow

---

## Data Model

### 1. Tenant
Represents a client company using the platform.

Fields:
- id
- name
- created_at

Why:
Breathe ESG supports multiple enterprise customers. Every uploaded dataset and normalized record must belong to a tenant to ensure isolation between clients.

---

### 2. DataSource
Represents an ingestion source event.

Fields:
- tenant (FK)
- source_type (SAP / UTILITY / TRAVEL)
- file_name
- uploaded_by
- uploaded_at

Why:
Tracks source-of-truth metadata for every ingestion event.

This helps answer:
- where did this data come from?
- who uploaded it?
- when was it uploaded?

---

### 3. RawRecord
Stores raw source data before normalization.

Fields:
- data_source (FK)
- raw_payload (JSON)
- validation_status

Why:
Raw source preservation is critical for auditability.

Auditors or analysts may need to compare normalized ESG records against the original uploaded source.

This supports:
- traceability
- debugging ingestion failures
- future parser improvements

---

### 4. NormalizedRecord
Stores ESG-standardized records for review.

Fields:
- tenant (FK)
- raw_record (FK)
- activity_type
- scope
- original_value
- original_unit
- normalized_value
- normalized_unit
- suspicious
- status
- created_at

Status values:
- PENDING
- APPROVED
- REJECTED
- LOCKED
- FAILED

Why:
Different source systems provide inconsistent schemas.

Normalization transforms them into a consistent ESG review model.

Example:
SAP fuel liters → Scope 1
Utility electricity kWh → Scope 2
Travel distance km → Scope 3

Suspicious flag:
Used to surface records needing analyst review.

Examples:
- unusually large fuel consumption
- unusually high electricity usage
- flights with zero distance

---

### 5. AuditLog
Tracks analyst actions.

Fields:
- record (FK)
- action
- changed_by
- changed_at

Actions:
- APPROVED
- REJECTED
- LOCKED

Why:
Required for audit traceability.

Supports questions like:
- who approved this?
- when was it locked?
- was it modified after review?

---

## ESG Scope Mapping

### Scope 1
Direct emissions.

Mapped source:
- SAP fuel procurement

Example:
Diesel fuel consumption

---

### Scope 2
Purchased electricity.

Mapped source:
- utility consumption

Example:
kWh from utility export

---

### Scope 3
Indirect operational emissions.

Mapped source:
- travel

Examples:
- flights
- hotels
- ground transport

---

## Unit Normalization

Current prototype normalizes:
- fuel → liters
- electricity → kWh
- travel → km

Future versions should support:
- gallons → liters
- MWh → kWh
- miles → km

---

## Audit Workflow

Flow:
UPLOAD → NORMALIZE → REVIEW → APPROVE/REJECT → LOCK

FAILED records are separated for analyst visibility.

LOCK prevents further modification before audit review.

---

## Multi-Tenancy

All business data is tenant-scoped:
- DataSource
- NormalizedRecord

This prevents data leakage across enterprise clients.

---

## Design Philosophy

This prototype intentionally separates:
raw ingestion
normalized ESG review
audit tracking

This keeps ingestion flexible while preserving audit integrity.