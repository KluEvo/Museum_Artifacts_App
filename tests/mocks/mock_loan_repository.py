from src.domain.loan import Loan
from datetime import datetime, timezone
from typing import List

class MockLoanRepository:
    def get_loan_by_id(self, loan_id):
        mock = Loan(
            loan_id = 'mock_id', 
            start_date = '2000-01-02T00:00:00', 
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

