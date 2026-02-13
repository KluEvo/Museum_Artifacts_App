import pytest

from src.domain.loan import Loan
import src.services.loan_service as loan_service
from tests.mocks.mock_loan_repository import MockLoanRepository
from src.exceptions import ValidationException
from datetime import datetime, timezone


def test_add_loan_positive():
    repo = MockLoanRepository()
    svc = loan_service.LoanService(repo)
    loan = Loan(
        loan_id = 'mock_id', 
        start_date = '2000-01-02T00:00:00', 
        end_date = None, 
        loan_status = 'test', 
        insurance_value = 'test'
    )
    loan_id = svc.add_loan(loan)
    assert loan_id == 'mock_id'

def test_remove_loan_positive():
    repo = MockLoanRepository()
    svc = loan_service.LoanService(repo)
    loan_id = svc.remove_loan('mock_id')
    assert loan_id == 'mock_id'

def test_update_loan_positive():
    repo = MockLoanRepository()
    svc = loan_service.LoanService(repo)
    loan_id = svc.remove_loan('mock_id')
    assert loan_id == 'mock_id'
