from typing import List, Protocol
from src.domain.loan import Loan

class LoanRepositoryProtocol(Protocol):
    def get_all_loans(self) -> List[Loan]:
        ...

    def add_loan(self, loan: Loan) -> str:
        ...

    def get_loan_by_id(self, loan_id: str) -> Loan:
        ...
        
    def remove_loan(self, loan_id: str) -> str:
        ...

    def update_loan(self, loan_id: str, updated_fields_dict: dict) -> str:
        ...
    
    
