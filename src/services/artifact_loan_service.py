from src.repositories.artifact_loan_repository_protocol import ArtifactLoanRepositoryProtocol
from src.domain.artifact_loan import ArtifactLoan
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from src.exceptions import (
    AppErrorException,
    ValidationException,
    NotFoundException,
)
import logging
logger = logging.getLogger(__name__)


class ArtifactLoanService:
    def __init__(self, artifact_loan_repo: ArtifactLoanRepositoryProtocol):
        self.artifact_loan_repo = artifact_loan_repo

    def add_artifact_loan(self, artifact_loan: ArtifactLoan) -> str:
        if not isinstance(artifact_loan, ArtifactLoan):
            raise ValidationException("Invalid ArtifactLoan object provided.")

        try:
            return str(self.artifact_loan_repo.add_artifact_loan(artifact_loan))
        except SQLAlchemyError as e:
            logger.exception("Database error while adding artifact loan")
            raise AppErrorException(
                "Database error occurred while adding artifact loan."
            ) from e

    def get_artifact_loan_by_ids(self, artifact_id: str, loan_id: str) -> ArtifactLoan:
        if not isinstance(artifact_id, str) or not isinstance(loan_id, str):
            raise ValidationException("Artifact ID and Loan ID must be strings.")

        try:
            artifact_loan = self.artifact_loan_repo.get_artifact_loan_by_id(artifact_id, loan_id)
            if artifact_loan is None:
                raise NotFoundException(
                    f"ArtifactLoan with artifact_id {artifact_id} and loan_id {loan_id} not found."
                )
            return artifact_loan
        except SQLAlchemyError as e:
            logger.exception("Database error while adding artifact loan")
            raise AppErrorException(
                "Database error occurred while retrieving artifact loan."
            ) from e

    def get_artifact_loans_by_artifact(self, artifact_id: str) -> List[ArtifactLoan]:
        if not isinstance(artifact_id, str):
            raise ValidationException("Artifact ID must be a string.")

        try:
            loans = self.artifact_loan_repo.get_artifact_loans_by_artifact(artifact_id)
            if not loans:
                raise NotFoundException(f"No artifact loans found for artifact_id {artifact_id}.")
            return loans
        except SQLAlchemyError as e:
            logger.exception("Database error while retrieving artifact loans for artifact_id=%s", artifact_id)
            raise AppErrorException(
                "Database error occurred while retrieving artifact loans by artifact."
            ) from e

    def get_artifact_loans_by_loan(self, loan_id: str) -> List[ArtifactLoan]:
        if not isinstance(loan_id, str):
            raise ValidationException("Loan ID must be a string.")

        try:
            loans = self.artifact_loan_repo.get_artifact_loans_by_loan(loan_id)
            if not loans:
                raise NotFoundException(f"No artifact loans found for loan_id {loan_id}.")
            return loans
        except SQLAlchemyError as e:
            logger.exception("Database error while retrieving artifact loans for loan_id=%s", loan_id)
            raise AppErrorException(
                "Database error occurred while retrieving artifact loans by loan."
            ) from e
