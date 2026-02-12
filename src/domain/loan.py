import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.base import Base

class Loan(Base):
    __tablename__ = 'loans'
    loan_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start_date= Column(DateTime, default = datetime.now(timezone.utc))
    end_date= Column(DateTime, nullable=True)
    loan_status= Column(String, nullable=False)
    insurance_value= Column(String, nullable=False)
    
    to_museum_id= Column(UUID(as_uuid=True), ForeignKey("museums.museum_id"), nullable=False)
    from_museum_id= Column(UUID(as_uuid=True), ForeignKey("museums.museum_id"), nullable=True)

    