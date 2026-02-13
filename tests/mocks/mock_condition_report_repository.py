from src.domain.condition_report import ConditionReport
from typing import List
from datetime import datetime, timezone
import uuid

class MockConditionReportRepository:
    def get_all_reports(self) -> List[ConditionReport]:
        return "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

    def add_report(self, report: ConditionReport) -> ConditionReport:
        return "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

    def get_report_by_id(self, report_id: str) -> ConditionReport:
        return ConditionReport(
                report_id=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
                artifact_id=uuid.UUID("bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
                report_date=datetime(2020, 1, 1, tzinfo=timezone.utc),
                condition_rating=4.5,
                notes="Mock condition report",
            )

    def get_reports_by_artifact(self, artifact_id: str) -> List[ConditionReport]:
        return [
                ConditionReport(
                    report_id=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
                    artifact_id=uuid.UUID("bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
                    report_date=datetime(2020, 1, 1, tzinfo=timezone.utc),
                    condition_rating=4.5,
                    notes="Mock condition report 1",
                ),
                ConditionReport(
                    report_id=uuid.UUID("aaaaaaaa-bbbb-aaaa-aaaa-aaaaaaaaaaaa"),
                    artifact_id=uuid.UUID("bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
                    report_date=datetime(2021, 1, 1, tzinfo=timezone.utc),
                    condition_rating=4.0,
                    notes="Mock condition report 2",
                ),
            ]

    def update_report(self, report_id: str, updated_fields_dict: dict) -> str:
        if report_id != "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa":
            return None
        
        return ConditionReport(
            report_id=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            artifact_id=uuid.UUID(
                updated_fields_dict.get(
                    "artifact_id", 
                    "bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
                )
            ),
            report_date=updated_fields_dict.get(
                "report_date", 
                 datetime(2020, 1, 1, tzinfo=timezone.utc)
            ),
            condition_rating=updated_fields_dict.get(
                "condition_rating", 
                 4.5
            ),
            notes=updated_fields_dict.get(
                "notes",
                "Mock condition report"
            )
        )

    def remove_report(self, report_id: str) -> str:
        if report_id == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa":
            return report_id
        return None