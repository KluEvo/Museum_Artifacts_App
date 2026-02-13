from typing import List, Protocol
from src.domain.condition_report import ConditionReport

class ConditionReportRepositoryProtocol(Protocol):
    def get_all_reports(self) -> List[ConditionReport]:
        ...

    def add_condition_report(self, report: ConditionReport) -> str:
        ...

    def get_condition_report_by_id(self, report_id: str) -> ConditionReport:
        ...

    def get_reports_by_artifact(self, artifact_id: str) -> List[ConditionReport]:
        ...

    def update_condition_report(self, report_id: str, updated_fields_dict: dict) -> str:
        ...

    def remove_condition_report(self, report_id: str) -> str:
        ...
