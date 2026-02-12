from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class LoanCreate(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    loan_status: Optional[str] = None
    insurance_value: Optional[str] = None
    to_museum_id: UUID
    from_museum_id: UUID


class LoanRead(LoanCreate):
    loan_id: UUID
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    loan_status: Optional[str] = None
    insurance_value: Optional[str] = None
    to_museum_id: UUID
    from_museum_id: UUID

    class Config:
        from_attributes = True


class LoanUpdate(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    loan_status: Optional[str] = None
    insurance_value: Optional[str] = None
    to_museum_id: Optional[UUID] = None
    from_museum_id: Optional[UUID] = None
