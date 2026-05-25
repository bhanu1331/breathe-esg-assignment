# SOURCES.md

## Overview
This prototype was designed after researching realistic enterprise ESG data ingestion patterns.

The goal was not to simulate ideal clean APIs, but to model how operational data commonly reaches ESG reporting systems in real organizations.

This document explains the real-world source assumptions, why certain formats were chosen, what the sample data represents, and what limitations remain.

---

# 1. SAP Source (Fuel / Procurement Data)

## Real-world source research
SAP enterprise data can be exposed through multiple integration mechanisms:

- IDoc
- BAPI
- OData services
- Flat file exports (CSV / Excel)

For ESG workflows, especially in prototype and manual reporting scenarios, flat-file exports are still common because procurement and finance teams frequently export operational data for reconciliation.

---

## Chosen prototype format
CSV upload representing SAP flat export.

Reason:
This allowed realistic ingestion without requiring SAP credentials, API setup, or environment dependencies.

This matches a practical onboarding scenario where a client provides exported operational extracts.

---

## Sample data design
The SAP sample includes:

- Document Number
- Plant Code
- Material Description
- Quantity
- Unit
- Posting Date
- Vendor

Example:

Diesel fuel procurement records.

Why:
These fields realistically represent procurement-style operational activity relevant to Scope 1 emissions.

Example ESG interpretation:
Fuel purchased for operational consumption.

---

## Real-world challenges identified
SAP data can be difficult because:

- inconsistent export schemas
- cryptic plant identifiers
- procurement category ambiguity
- German/localized headers
- inconsistent date formats
- mixed units

Examples:
- Liter vs gallons
- DD.MM.YYYY vs ISO dates
- abbreviated material descriptions

---

## Production limitations
Not implemented:

- SAP authentication
- OData integration
- IDoc parsing
- BAPI connectors
- plant lookup resolution
- multilingual field normalization
- procurement hierarchy parsing

---

# 2. Utility Electricity Source

## Real-world source research
Utility data commonly reaches enterprise ESG systems through:

- provider web portal CSV export
- PDF utility bills
- utility APIs (when available)

Facilities teams often manually download electricity usage reports.

---

## Chosen prototype format
CSV upload representing utility portal export.

Reason:
CSV is structured, deterministic, and practical for a prototype.

PDF parsing would require OCR and document extraction logic that is outside prototype scope.

---

## Sample data design
The utility sample includes:

- Meter ID
- Billing Start
- Billing End
- Consumption
- Unit
- Tariff

Why:
These fields are typical of electricity usage exports.

Example:
Monthly electricity consumption from a facility meter.

Mapped ESG interpretation:
Scope 2 purchased electricity.

---

## Real-world challenges identified
Utility data often includes:

- multiple meters
- inconsistent billing cycles
- tariff complexity
- demand vs consumption confusion
- mixed units

Examples:
- MWh vs kWh
- overlapping billing periods
- estimated usage corrections

---

## Production limitations
Not implemented:

- PDF parsing
- OCR extraction
- utility APIs
- tariff cost modeling
- billing normalization
- multi-meter aggregation

---

# 3. Corporate Travel Source

## Real-world source research
Corporate travel systems commonly expose data through:

- CSV reports
- API integrations
- scheduled exports

Platforms researched conceptually:

- SAP Concur
- Navan
- similar enterprise travel management systems

---

## Chosen prototype format
CSV upload representing travel export.

Reason:
Travel reporting exports are realistic and easier to prototype than authenticated API integrations.

---

## Sample data design
The travel sample includes:

- Trip ID
- Employee
- Category
- From
- To
- Distance
- Distance Unit

Supported categories:

- Flight
- Hotel
- Taxi

Why:
These categories reflect common Scope 3 travel activity.

A suspicious example was included:

Flight with zero distance.

This demonstrates anomaly review workflow.

---

## Real-world challenges identified
Travel datasets often contain:

- airport codes only
- missing route distances
- hotel nights instead of emissions values
- mixed transport categories
- duplicate itinerary segments

Examples:
- HYD → BOM without explicit distance
- business class vs economy differentiation
- taxi receipts with incomplete metadata

---

## Production limitations
Not implemented:

- API authentication
- airport distance lookup
- itinerary stitching
- hotel emissions factor mapping
- travel class differentiation
- duplicate detection

---

# Why CSV was chosen for all sources
This was a deliberate prototype decision.

CSV upload offers:

- realistic onboarding simulation
- deterministic testability
- simpler validation
- faster prototype delivery

In real enterprise onboarding, exported operational files are often the first integration step before deeper API automation.

---

# Design philosophy
The prototype prioritizes:

- realistic ingestion architecture
- analyst review workflow
- audit traceability
- explainable implementation decisions

over production-complete integrations.