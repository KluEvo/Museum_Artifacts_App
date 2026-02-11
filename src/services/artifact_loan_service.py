from src.repositories.artifact_loan_repository_protocol import ArtifactLoanRepositoryProtocol
from src.domain.artifact_loan import ArtifactLoan
from src.domain.artifact import Artifact
from src.domain.loan import Loan

class ArtifactLoanService:
    def __init__(self, artifact_loan_repo: ArtifactLoanRepositoryProtocol):
        self.artifact_loan_repo = artifact_loan_repo
        
    def add_artifact_loan(self, artifact_loan: ArtifactLoan) -> str:
        return str(self.artifact_loan_repo.add_artifact_loan(artifact_loan))
    
    def get_artifact_loan_by_ids(self, artifact_id: Artifact, loan_id: Loan) -> str:
        return str(self.artifact_loan_repo.get_artifact_loan_by_ids(artifact_id, loan_id))
    