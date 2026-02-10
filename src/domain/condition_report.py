import uuid
from sqlalchemy import Column, ForeignKey, String, Float, DateTime
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from src.base import Base

class ConditionReport(Base):
    __tablename__ = 'condition_reports'

    report_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    artifact_id = Column(UUID(as_uuid=True), nullable=False), ForeignKey("artifacts.artifact_id")
    report_date = Column(DateTime, nullable=False)
    condition_rating = Column(Float, nullable=False)
    notes = Column(String, nullable=True)
