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
* discovery_date
* estimated_value
* parent_artifact (id)
* museum_id (FK)


---

### Supporting Entities (2–3)

**`Museum`**

* museum_id (PK)
* name
* location
* contact_email

**`Loan`**

* loan_id (PK)
* start_date
* end_date
* to_museum_id(FK)
* from_museum_id(FK)
* loan_status
* insurance_value

**`ConditionReport`**

* report_id (PK)
* artifact_id (FK)
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

* `parent_artifact` (nullable FK to artifact_id)

Use cases:

* Artifact sets (e.g., armor + helmet)
* Composite artifacts
* Fragmented pieces of a single original item

---

## Endpoints

### Core CRUD

* `POST /artifacts`
Add artifact
* `GET /artifacts`
Get all artifacts
* `GET /artifacts/{id}`
Get artifact by id
* `PUT /artifacts/{id}`
Edit artifact by id
* `DELETE /artifacts/{id}`
Delete artifact by id
* `POST /loans`
add loan
* `GET /loans/{id}`
Get loan by id
* `PATCH /loans/{id}/status`
update loan status by id
* `DELETE /loans/{id}`
Delete loan by id
---

### Relationship-Based Endpoints (Required)

* `GET /artifacts/{id}/loan-history`

  * returns nested loan + museum info
* `GET /loans/{id}/artifacts`

  * returns artifacts + condition requirements

Optional extra 🔥:

* `GET /museums/{id}/outgoing-loans`
* `GET /artifacts/{id}/condition-reports`
