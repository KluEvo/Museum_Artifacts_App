from typing import List, Protocol
from src.domain.condition_report import ConditionReport

class ConditionReportRepositoryProtocol(Protocol):
    def add_report(self, report: ConditionReport) -> ConditionReport:
        ...

    def get_report_by_id(self, report_id: str) -> ConditionReport:
        ...

    def get_reports_by_artifact(self, artifact_id: str) -> List[ConditionReport]:
        ...

    def update_report(self, report_id: str, updated_fields_dict: dict) -> str:
        ...

    def remove_report(self, report_id: str) -> str:
        ...