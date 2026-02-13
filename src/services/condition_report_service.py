from src.repositories.condition_report_repository_protocol import ConditionReportRepositoryProtocol
from src.domain.condition_report import ConditionReport
from sqlalchemy.exc import SQLAlchemyError
from src.exceptions import (
    AppErrorException,
    ValidationException,
    NotFoundException,
)


class ConditionReportService:
    def __init__(self, condition_report_repo: ConditionReportRepositoryProtocol):
        self.condition_report_repo = condition_report_repo

    def add_condition_report(self, condition_report: ConditionReport) -> str:
        if not isinstance(condition_report, ConditionReport):
            raise ValidationException("Invalid ConditionReport object provided.")

        try:
            return self.condition_report_repo.add_condition_report(condition_report)
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while adding condition report."
            ) from e
    
    def get_condition_report_by_id(self, condition_report_id: str) -> ConditionReport:
        if not isinstance(condition_report_id, str):
            raise ValidationException("ConditionReport ID must be a string.")

        try:
            report = self.condition_report_repo.get_report_by_id(condition_report_id)
            if report is None:
                raise NotFoundException(f"ConditionReport with id {condition_report_id} not found.")
            return report
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while retrieving condition report."
            ) from e

    def update_condition_report(self, condition_report_id: str, updated_fields_dict: dict) -> str:
        if not isinstance(condition_report_id, str):
            raise ValidationException("ConditionReport ID must be a string.")
        if not isinstance(updated_fields_dict, dict):
            raise ValidationException("Updated fields must be a dictionary.")

        try:
            updated_id = self.condition_report_repo.update_condition_report(
                condition_report_id, updated_fields_dict
            )
            if not updated_id:
                raise NotFoundException(f"ConditionReport with id {condition_report_id} not found.")
            return updated_id
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while updating condition report."
            ) from e
        
    def remove_condition_report(self, condition_report_id: str) -> str:
        if not isinstance(condition_report_id, str):
            raise ValidationException("ConditionReport ID must be a string.")

        try:
            removed_id = self.condition_report_repo.remove_condition_report(condition_report_id)
            if not removed_id:
                raise NotFoundException(f"ConditionReport with id {condition_report_id} not found.")
            return removed_id
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while removing condition report."
            ) from e
