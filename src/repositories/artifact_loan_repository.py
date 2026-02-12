from typing import List, Tuple
from sqlalchemy.orm import Session
from src.domain.artifact_loan import ArtifactLoan
from src.domain.loan import Loan
from src.domain.artifact import Artifact
from src.repositories.artifact_loan_repository_protocol import ArtifactLoanRepositoryProtocol

class ArtifactLoanRepository(ArtifactLoanRepositoryProtocol):

    def __init__(self, session : Session):
        self.session = session

    def add_artifact_loan(self, artifact_loan: ArtifactLoan) -> Tuple[str]:
        self.session.add(artifact_loan)
        self.session.commit()
        return (str(artifact_loan.artifact_id), str(artifact_loan.loan_id))


    def get_artifact_loan_by_id(self, artifact_id: str, loan_id: str) -> ArtifactLoan:
        return self.session.query(ArtifactLoan).filter(ArtifactLoan.artifact_id == artifact_id).filter(ArtifactLoan.loan_id == loan_id).first()

    def get_artifact_loans_by_artifact(self, artifact_id: str) -> List[ArtifactLoan]:
        return self.session.query(ArtifactLoan).filter(ArtifactLoan.artifact_id == artifact_id).all()
    
    def get_artifact_loans_by_loan(self, loan_id: str) -> List[ArtifactLoan]:
        return self.session.query(ArtifactLoan).filter(ArtifactLoan.loan_id == loan_id).all()
    
    def update_artifact_loan(self, artifact_id: str, loan_id: str, updated_fields_dict: dict) -> Tuple[str]:
        artifact_loan = self.get_artifact_loan_by_id(artifact_id, loan_id)
        if not artifact_loan:
            return None 

        allowed_fields = {col.name for col in ArtifactLoan.__table__.columns if not col.primary_key}

        for field, value in updated_fields_dict.items():
            if field not in allowed_fields:
                raise ValueError(f"Field not updatable: {field}")
            setattr(artifact_loan, field, value)

        self.session.commit()
        return (str(artifact_loan.artifact_id), str(artifact_loan.loan_id))
    
    def remove_artifact_loan(self, artifact_id: str, loan_id: str) -> Tuple[str]:
        artifact_loan = self.get_artifact_loan_by_id(artifact_id)
        self.session.delete(artifact_loan)
        self.session.commit()
        return (str(artifact_loan.artifact_id), str(artifact_loan.loan_id))