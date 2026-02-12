from src.repositories.artifact_loan_repository_protocol import ArtifactLoanRepositoryProtocol
from src.domain.artifact_loan import ArtifactLoan
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from src.exceptions import (
    AppErrorException,
    ValidationException,
    NotFoundException,
)

class ArtifactLoanService:
    def __init__(self, artifact_loan_repo: ArtifactLoanRepositoryProtocol):
        self.artifact_loan_repo = artifact_loan_repo

    def add_artifact_loan(self, artifact_loan: ArtifactLoan) -> str:
        if not isinstance(artifact_loan, ArtifactLoan):
            raise ValidationException("Invalid ArtifactLoan object provided.")

        try:
            return str(self.artifact_loan_repo.add_artifact_loan(artifact_loan))
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while adding artifact loan."
            ) from e

    def get_artifact_loan_by_ids(self, artifact_id: str, loan_id: str) -> ArtifactLoan:
        if not isinstance(artifact_id, str) or not isinstance(loan_id, str):
            raise ValidationException("Artifact ID and Loan ID must be strings.")

        try:
            return str(self.artifact_loan_repo.get_artifact_loan_by_id(artifact_id, loan_id))
        except ValueError:
            raise NotFoundException(
                f"ArtifactLoan with artifact_id {artifact_id} and loan_id {loan_id} not found."
            )
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while retrieving artifact loan."
            ) from e

    def get_artifact_loans_by_artifact(self, artifact_id: str) -> List[ArtifactLoan]:
        if not isinstance(artifact_id, str):
            raise ValidationException("Artifact ID must be a string.")

        try:
            return self.artifact_loan_repo.get_artifact_loans_by_artifact(artifact_id)
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while retrieving artifact loans by artifact."
            ) from e

    def get_artifact_loans_by_loan(self, loan_id: str) -> List[ArtifactLoan]:
        if not isinstance(loan_id, str):
            raise ValidationException("Loan ID must be a string.")

        try:
            return self.artifact_loan_repo.get_artifact_loans_by_loan(loan_id)
        except SQLAlchemyError as e:
            raise AppErrorException(
                "Database error occurred while retrieving artifact loans by loan."
            ) from e
