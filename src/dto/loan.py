from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from pydantic.config import ConfigDict

class LoanCreate(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    loan_status: Optional[str] = None
    insurance_value: Optional[str] = None
    to_museum_id: UUID
    from_museum_id: UUID


class LoanRead(LoanCreate):

    model_config = ConfigDict(from_attributes = True)
    loan_id: UUID
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    loan_status: Optional[str] = None
    insurance_value: Optional[str] = None
    to_museum_id: UUID
    from_museum_id: UUID


class LoanUpdate(BaseModel):

    model_config = ConfigDict(from_attributes = True)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    loan_status: Optional[str] = None
    insurance_value: Optional[str] = None
    to_museum_id: Optional[UUID] = None
    from_museum_id: Optional[UUID] = None
