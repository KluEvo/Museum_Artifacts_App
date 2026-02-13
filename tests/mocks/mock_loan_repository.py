from src.domain.loan import Loan
from datetime import datetime, timezone

class MockLoanRepository:
    def get_all_loans(self) -> List[Loan]:
        return [Loan(loan_id = 'mock_id', start_date = datetime.now(timezone.utc), end_date = None, loan_status = 'test', insurance_value = 'test')]
    
    def get_loan_by_id(self, loan_id):
        mock = Loan(
            loan_id = 'mock_id', 
            start_date = datetime.now(timezone.utc), 
            end_date = None, 
            loan_status = 'test', 
            insurance_value = 'test'
            )
        return mock
    
    def add_loan(self, loan: Loan) -> str:
        return 'mock_id'

    def remove_loan(self, loan_id: str) -> str:
        return 'mock_id'

    def update_loan(self, loan_id: str, updated_fields_dict: dict) -> str:
        return 'mock_id'