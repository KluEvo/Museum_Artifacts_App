from src.repositories.condition_report_repository_protocol import ConditionReportRepositoryProtocol
from src.domain.condition_report import ConditionReport

class ConditionReportService:
    def __init__(self, condition_report_repo: ConditionReportRepositoryProtocol):
        self.condition_report_repo = condition_report_repo

    def add_condition_report(self, condition_report: ConditionReport) -> str:
        return self.condition_report_repo.add_condition_report(condition_report)
    
    def get_condition_report_by_id(self, condition_report_id: str) -> str:
        if not isinstance(condition_report_id, str):
            raise TypeError('Expected str, got something else.')
        return self.condition_report_repo.get_condition_report_by_id(condition_report_id)

    def update_condition_report(self, condition_report_id: str, updated_fields_dict: dict) -> str:
        if not isinstance(condition_report_id, str):
            raise TypeError('Expected str, got something else.')
        if not isinstance(updated_fields_dict, dict):
            raise TypeError('Expected a dict, got something else.')
        return self.condition_report_repo.update_condition_report(condition_report_id, updated_fields_dict)
    
    def remove_condition_report(self, condition_report_id: str):
        if not isinstance(condition_report_id, str):
            raise TypeError('Expected str, got something else.')
        return self.condition_report_repo.remove_condition_report(condition_report_id)

