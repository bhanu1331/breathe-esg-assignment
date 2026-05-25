# SOURCES.md

## Overview
This document describes the real-world source formats researched for each ingestion pipeline, what assumptions were made, how sample data was modeled, and limitations for production deployment.

---

# 1. SAP Source Research

## Real-world formats researched
SAP enterprise data can be exposed through:

- IDoc
- BAPI
- OData services
- flat-file CSV / Excel exports

For this prototype, flat-file export was selected.

---

## Why this format was chosen
Although SAP supports API-based integrations, many enterprise ESG reporting workflows still rely on exported procurement and fuel extracts from finance or operations teams.

Flat-file ingestion is realistic because:
- finance teams often export CSVs for reconciliation
- easier prototype validation
- avoids SAP environment dependency
- simpler analyst testing workflow

---

## What was learned
SAP data is often messy.

Typical challenges:
- cryptic plant codes
- inconsistent units
- multilingual headers
- procurement category ambiguity
- date formatting inconsistencies

Examples:
- German labels
- material descriptions that require mapping
- internal vendor identifiers

---

## Sample data design
Prototype SAP sample:

Fields:
- Document Number
- Plant Code
- Material Description
- Quantity
- Unit
- Posting Date
- Vendor

Why:
These represent a simplified but plausible fuel procurement export.

Example use case:
Diesel procurement records later mapped into Scope 1 operational activity.

---

## What would break in production
This prototype does not handle:
- SAP authentication
- OData pagination
- IDoc parsing
- multilingual header normalization
- plant lookup mapping
- procurement category disambiguation
- schema drift

Production implementation would require configurable ingestion adapters.

---

# 2. Utility Source Research

## Real-world formats researched
Utility data commonly arrives through:

- utility web portal CSV export
- PDF bills
- utility APIs (less common depending on provider)

For this prototype, CSV export was selected.

---

## Why this format was chosen
Facilities teams frequently export billing data manually from utility portals.

Compared to PDF parsing:
CSV is:
- structured
- deterministic
- easier to validate
- better for rapid prototyping

---

## What was learned
Utility datasets often include:
- meter identifiers
- billing periods
- tariff classes
- demand vs consumption values
- inconsistent unit scales

Challenges:
- multiple meters
- overlapping billing periods
- cost vs consumption confusion
- MWh vs kWh normalization

---

## Sample data design
Prototype utility sample:

Fields:
- Meter ID
- Billing Start
- Billing End
- Consumption
- Unit
- Tariff

Why:
Represents realistic exported portal billing consumption data.

Example:
commercial electricity usage mapped into Scope 2.

---

## What would break in production
Not handled:
- PDF OCR parsing
- multi-meter aggregation
- provider-specific schemas
- utility authentication
- API integrations
- demand charges
- month boundary normalization

Production would need ingestion adapters and validation rules.

---

# 3. Travel Source Research

## Real-world formats researched
Corporate travel systems researched conceptually:

- SAP Concur
- Navan
- similar enterprise travel platforms

Typical data includes:
- flights
- hotels
- rail
- taxis
- trip metadata

For prototype simplicity, CSV export was selected.

---

## Why this format was chosen
Travel platforms often provide downloadable reports.

CSV export allowed realistic simulation without API authentication complexity.

---

## What was learned
Travel datasets may contain:
- airport codes
- itinerary segments
- booking references
- hotel nights
- transport categories

Challenges:
- missing distances
- airport-only location identifiers
- emission factor differences by class
- multi-leg trip decomposition

---

## Sample data design
Prototype travel sample:

Fields:
- Trip ID
- Employee
- Category
- From
- To
- Distance
- Distance Unit

Included:
- flight
- hotel
- taxi
- suspicious flight with zero distance

Why:
Demonstrates analyst review of both valid and suspicious travel activity.

---

## What would break in production
Not handled:
- Concur authentication
- Navan APIs
- airport distance resolution
- hotel emissions modeling
- class-of-travel factors
- itinerary stitching
- duplicate trip imports

Production would likely use direct API ingestion with enrichment logic.

---

# Source selection summary

Prototype ingestion choices:

SAP → flat export CSV  
Utility → portal CSV export  
Travel → corporate travel CSV export

These choices prioritize:
- realism
- explainability
- deterministic testing
- prototype delivery speed