from typing import List, Tuple, Protocol
from src.domain.artifact_loan import ArtifactLoan
from src.domain.loan import Loan
from src.domain.artifact import Artifact

class ArtifactLoanRepositoryProtocol(Protocol):

    def add_artifact_loan(self, artifactLoan: ArtifactLoan) -> Tuple[str]:
        ...

    def get_artifact_loan_by_id(self, artifact_id: str, loan_id: str) -> ArtifactLoan:
        ...

    def update_artifact_loan(self, artifact_loan: ArtifactLoan) -> Tuple[str]:
        ...
    
    def remove_artifact_loan(self, artifact_id: str, loan_id: str) -> Tuple[str]:
        ...