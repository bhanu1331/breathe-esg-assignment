# TRADEOFFS.md

## Overview
Given the 4-day assignment timeline, I prioritized building a complete end-to-end ESG ingestion and analyst review workflow rather than attempting production-grade completeness.

The goal was to demonstrate sound architectural judgment, auditability, and realistic workflow design.

Below are deliberate tradeoffs made during implementation.

---

# 1. API integrations were not implemented

## What was not built
Direct integrations with:
- SAP OData / BAPI / IDoc
- utility provider APIs
- Concur / Navan APIs

## Why
Real integrations require:
- authentication flows
- credential management
- retry logic
- rate limiting
- API schema handling
- webhook/event processing

This would significantly increase implementation complexity and reduce time available for core workflow design.

Instead, CSV upload ingestion was chosen because exported flat files are still common in enterprise ESG workflows.

## Tradeoff
Pros:
- faster prototype delivery
- realistic ingestion simulation
- simpler testing

Cons:
- no live source synchronization
- manual upload dependency

---

# 2. Advanced normalization logic was simplified

## What was not built
Full unit conversion engine for:
- gallons → liters
- MWh → kWh
- miles → kilometers
- fuel-type-specific normalization

## Why
The assignment focused primarily on ingestion architecture and analyst workflow.

A complete conversion engine requires:
- unit dictionaries
- conversion factor validation
- error handling for unsupported units
- source-specific transformation logic

For this prototype, normalization structure exists, but conversion behavior was simplified.

## Tradeoff
Pros:
- clear architecture
- easier explainability
- faster delivery

Cons:
- less realistic transformation accuracy

---

# 3. Emissions calculation engine was intentionally excluded

## What was not built
Actual carbon emissions calculation using emission factors.

Examples:
- kgCO₂e per kWh
- flight route emissions
- hotel room-night factors
- fuel-specific factors

## Why
The assignment emphasized ingestion, normalization, auditability, and analyst review—not carbon computation.

Adding emissions calculations would introduce:
- methodology assumptions
- regional factor dependencies
- versioning complexity

This was intentionally left out to keep scope focused.

## Tradeoff
Pros:
- cleaner prototype focus
- avoids questionable assumptions

Cons:
- incomplete ESG reporting functionality

---

# 4. Full authentication and RBAC were not implemented

## What was not built
Production-grade access control:
- tenant-specific authentication
- analyst/admin role separation
- permission enforcement
- JWT/session auth workflows

## Why
The assignment focused on prototype functionality.

Implementing robust auth would require significant additional backend work without improving ingestion architecture evaluation.

Django admin and tenant association demonstrate structural readiness.

## Tradeoff
Pros:
- faster delivery
- simpler architecture

Cons:
- not production secure

---

# 5. Real-world messy source parsing was partially simplified

## What was not built
Handling for:
SAP:
- German headers
- plant code mapping
- date normalization
- procurement hierarchies

Utility:
- PDF OCR parsing
- tariff interpretation
- billing period reconciliation

Travel:
- airport code route inference
- cabin class differentiation
- hotel night normalization

## Why
These represent production-scale complexity beyond prototype scope.

The ingestion architecture was designed so these enhancements can be added later.

## Tradeoff
Pros:
- realistic MVP scope
- cleaner prototype

Cons:
- narrower source realism

---

# 6. Edit-after-approval workflow was excluded

## What was not built
Manual analyst correction workflows.

Example:
- edit suspicious value
- reprocess normalized output
- version compare changes

## Why
The assignment required review + sign-off workflow.

Approve / reject / lock satisfies this requirement.

Editable correction workflows would require:
- version tracking
- change auditing
- reconciliation logic

## Tradeoff
Pros:
- simpler governance workflow

Cons:
- reduced analyst flexibility

---

# 7. Frontend UX was optimized for clarity, not production polish

## What was not built
Advanced UX features:
- pagination
- sorting
- search
- record detail drawer
- inline editing
- bulk approve/reject

## Why
The goal was analyst usability, not enterprise frontend completeness.

The dashboard demonstrates review workflow clearly.

## Tradeoff
Pros:
- focused UX
- simpler implementation

Cons:
- limited scalability