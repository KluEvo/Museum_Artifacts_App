import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from src.base import Base


class ArtifactLoan(Base):
    __tablename__ = 'artifact_loans'
    #Make composite key
    artifact_id = Column(UUID(as_uuid=True), ForeignKey('artifacts.artifact_id'), primary_key=True)
    loan_id = Column(UUID(as_uuid=True), ForeignKey('loans.loan_id'), primary_key=True)
    display_requirements = Column(String, nullable=True)
    return_condition_required = Column(String, nullable=True)

