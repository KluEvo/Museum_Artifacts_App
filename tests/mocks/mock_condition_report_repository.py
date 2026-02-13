from src.domain.condition_report import ConditionReport
from typing import List
from datetime import datetime, timezone
import uuid

class MockConditionReportRepository:

    def get_all_reports(self) -> List[ConditionReport]:
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

    def add_condition_report(self, report: ConditionReport) -> str:
        return "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

    def get_condition_report_by_id(self, report_id: str) -> ConditionReport:
        if report_id == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa":
            return ConditionReport(
                report_id=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
                artifact_id=uuid.UUID("bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
                report_date=datetime(2020, 1, 1, tzinfo=timezone.utc),
                condition_rating=4.5,
                notes="Mock condition report",
            )
        return None

    def get_reports_by_artifact(self, artifact_id: str) -> List[ConditionReport]:
        if artifact_id == "bbbbbbbb-aaaa-aaaa-aaaa-aaaaaaaaaaaa":
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
        return []

    def update_condition_report(self, report_id: str, updated_fields_dict: dict) -> str:
        if report_id == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa":
            return report_id
        return None

    def remove_condition_report(self, report_id: str) -> str:
        if report_id in [
            "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "aaaaaaaa-bbbb-aaaa-aaaa-aaaaaaaaaaaa",
            "aaaaaaaa-cccc-aaaa-aaaa-aaaaaaaaaaaa",
        ]:
            return report_id
        return None
