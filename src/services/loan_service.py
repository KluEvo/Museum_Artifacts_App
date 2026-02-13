from src.repositories.loan_repository_protocol import LoanRepositoryProtocol
from src.domain.loan import Loan
from sqlalchemy.exc import SQLAlchemyError
from src.exceptions import (
    AppErrorException,
    ValidationException,
    NotFoundException,
)


class LoanService:
    def __init__(self, loan_repo: LoanRepositoryProtocol):
        self.loan_repo = loan_repo

    def add_loan(self, loan: Loan) -> str:
        if not isinstance(loan, Loan):
            raise ValidationException("Invalid Loan object provided.")
        
        try:
            return self.loan_repo.add_loan(loan)
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while adding loan."
            ) from e
    
    def get_loan_by_id(self, loan_id: str) -> Loan:
        if not isinstance(loan_id, str):
            raise ValidationException("Loan ID must be a string.")

        try:
            loan = self.loan_repo.get_loan_by_id(loan_id)
            if loan is None:
                raise NotFoundException(f"Loan with id {loan_id} not found.")
            return loan
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while retrieving loan."
            ) from e

    def update_loan(self, loan_id: str, updated_fields_dict: dict) -> str:
        if not isinstance(loan_id, str):
            raise ValidationException("Loan ID must be a string.")
        if not isinstance(updated_fields_dict, dict):
            raise ValidationException("Updated fields must be a dictionary.")

        try:
            updated_id = self.loan_repo.update_loan(loan_id, updated_fields_dict)
            if not updated_id:
                raise NotFoundException(f"Loan with id {loan_id} not found.")
            return updated_id
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while updating loan."
            ) from e
    
    def remove_loan(self, loan_id: str) -> str:
        if not isinstance(loan_id, str):
            raise ValidationException("Loan ID must be a string.")

        try:
            removed_id = self.loan_repo.remove_loan(loan_id)
            if not removed_id:
                raise NotFoundException(f"Loan with id {loan_id} not found.")
            return removed_id
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while removing loan."
            ) from e
