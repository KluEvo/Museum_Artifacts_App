from typing import List
from sqlalchemy.orm import Session
from src.domain.loan import Loan
from src.repositories.loan_repository_protocol import LoanRepositoryProtocol

class LoanRepository(LoanRepositoryProtocol):
    def __init__(self, session: Session):
        self.session = session

    def get_all_loans(self) -> List[Loan]:
        return self.session.query(Loan).all()
    
    def get_loan_by_id(self, loan_id) -> Loan:
        return self.session.query(Loan).filter(Loan.loan_id == loan_id).first()
    
    def add_loan(self, loan: Loan) -> str:
        self.session.add(loan)
        self.session.commit()
        return str(loan.loan_id)

    def remove_loan(self, loan_id: str) -> str:
        loan = self.session.get(Loan, loan_id)
        if loan is None:
            return None

        self.session.delete(loan)
        self.session.commit()
        return str(loan_id)

    def update_loan(self, loan_id: str, updated_fields_dict: dict) -> str:
        loan = self.session.get(Loan, loan_id)
        if loan is None:
            return None
        
        allowed_fields = {col.name for col in Loan.__table__.columns if not col.primary_key}

        for field, value in updated_fields_dict.items():
            if field not in allowed_fields:
                raise ValueError(f"Field not updatable: {field}")
            setattr(loan, field, value)

        self.session.commit()
        self.session.refresh(loan)
        return str(loan.loan_id)