# Run from project root:
#   python scripts/export_museum_snapshot.py
#
import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine


# --- Database Connection ---
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/museum",
)


# --- Export Location ---
EXPORT_DIR = Path(__file__).resolve().parents[1] / "exports"
EXPORT_PATH = EXPORT_DIR / "museum_snapshot.json"


# --- Full Analytics Query ---
QUERY = """
WITH latest_condition AS (
  SELECT DISTINCT ON (cr.artifact_id)
    cr.artifact_id,
    cr.report_id,
    cr.report_date,
    cr.condition_rating,
    cr.notes
  FROM condition_reports cr
  ORDER BY cr.artifact_id, cr.report_date DESC
)
SELECT
  a.artifact_id,
  a.accession_number,
  a.name AS artifact_name,
  a.discovery_date,
  a.estimated_value,
  a.parent_artifact AS parent_artifact_id,
  a.museum_id AS owning_museum_id,

  om.name AS owning_museum_name,
  om.location AS owning_museum_location,
  om.contact_email AS owning_museum_contact_email,

  al.loan_id,
  al.display_requirements,
  al.return_condition_required,

  l.start_date AS loan_start_date,
  l.end_date AS loan_end_date,
  l.loan_status,
  l.insurance_value,
  l.to_museum_id,
  l.from_museum_id,

  tm.name AS to_museum_name,
  tm.location AS to_museum_location,
  tm.contact_email AS to_museum_contact_email,

  fm.name AS from_museum_name,
  fm.location AS from_museum_location,
  fm.contact_email AS from_museum_contact_email,

  lc.report_id AS latest_report_id,
  lc.report_date AS latest_report_date,
  lc.condition_rating AS latest_condition_rating,
  lc.notes AS latest_condition_notes

FROM artifact_loans al
JOIN artifacts a ON a.artifact_id = al.artifact_id

LEFT JOIN museums om ON om.museum_id = a.museum_id
JOIN loans l ON l.loan_id = al.loan_id

LEFT JOIN museums tm ON tm.museum_id = l.to_museum_id
LEFT JOIN museums fm ON fm.museum_id = l.from_museum_id

LEFT JOIN latest_condition lc ON lc.artifact_id = a.artifact_id

ORDER BY l.start_date DESC, a.accession_number;
"""


def main():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    engine = create_engine(DATABASE_URL)

    df = pd.read_sql_query(QUERY, engine)

    # Export JSON only
    df.to_json(EXPORT_PATH, orient="records", date_format="iso", indent=2)

    print(f"Exported {len(df)} rows to {EXPORT_PATH}")


if __name__ == "__main__":
    main()
