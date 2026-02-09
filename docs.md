## Museum Artifact Loan Management System

### Core Concept

A backend system for museums to track:

* Artifacts in their collection
* Loans to other museums or institutions
* Loan agreements, conditions, and history
* Conservation and inspection records

---

## 1. Data Model & ERD

### Core Entity

**`Artifact`**

* artifact_id (PK)
* name
* accession_number
* origin_date
* estimated_value
* condition_status


---

### Supporting Entities (2–3)

**`Museum`**

* museum_id
* name
* location
* contact_email

**`Loan`**

* loan_id
* start_date
* end_date
* loan_status
* insurance_value

**`ConditionReport`**

* report_id
* report_date
* condition_rating
* notes

---

### Junction Table (Many-to-Many)

**`ArtifactLoan`**

* artifact_id (FK)
* loan_id (FK)
* display_requirements
* return_condition_required

> One loan can include multiple artifacts
> One artifact can be loaned many times over its life

---

## Required Relationship Types

### One-to-Many

* Museum → Artifacts (owning museum)
* Loan → ConditionReports
* Artifact → ConditionReports

### Many-to-Many

* Artifacts ↔ Loans (via ArtifactLoan)

### Self-Relationship

**Artifact → Artifact**

* `parent_artifact_id` (nullable FK to artifact_id)

Use cases:

* Artifact sets (e.g., armor + helmet)
* Composite artifacts
* Fragmented pieces of a single original item

---

## Table Complexity

Every table easily has:

* Multiple non-trivial fields
* Dates, enums, decimals, text
* Constraints (unique accession_number, date checks, etc.)


## Endpoints

### Core CRUD

* `POST /artifacts`

* `GET /artifacts`

* `GET /artifacts/{id}`

* `PUT /artifacts/{id}`

* `DELETE /artifacts/{id}`

* `POST /loans`

* `GET /loans/{id}`

* `PATCH /loans/{id}/status`

* `DELETE /loans/{id}`

---

### Relationship-Based Endpoints (Required)

* `GET /artifacts/{id}/loan-history`

  * returns nested loan + museum info
* `GET /loans/{id}/artifacts`

  * returns artifacts + condition requirements

Optional extra 🔥:

* `GET /museums/{id}/outgoing-loans`
* `GET /artifacts/{id}/condition-reports`
