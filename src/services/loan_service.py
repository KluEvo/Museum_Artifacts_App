from src.repositories.loan_repository_protocol import LoanRepositoryProtocol
from src.domain.loan import Loan

class LoanService:
    def __init__(self, loan_repo: LoanRepositoryProtocol):
        self.loan_repo = loan_repo

    def add_loan(self, loan: Loan) -> str:
        return self.loan_repo.add_loan(loan)
    
    def get_loan_by_id(self, loan_id: str) -> str:
        if not isinstance(loan_id, str):
            raise TypeError('Expected str, got something else.')
        return self.loan_repo.get_loan_by_id(loan_id)

    def update_loan(self, loan_id: str, updated_fields_dict: dict) -> str:
        if not isinstance(loan_id, str):
            raise TypeError('Expected str, got something else.')
        if not isinstance(updated_fields_dict, dict):
            raise TypeError('Expected a dict, got something else.')
        return self.loan_repo.update_loan(loan_id, updated_fields_dict)
    
    def remove_loan(self, loan_id: str):
        if not isinstance(loan_id, str):
            raise TypeError('Expected str, got something else.')
        return self.loan_repo.remove_loan(loan_id)

