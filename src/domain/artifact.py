import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.base import Base

class Artifact(Base):
    __tablename__ = "artifacts"

    artifact_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    accession_number = Column(String, nullable=False)
    name = Column(String, nullable=False)
    discovery_date = Column(DateTime, nullable=True)
    estimated_value = Column(Integer, nullable=True)    
    
    parent_artifact = Column(UUID(as_uuid=True), ForeignKey("artifacts.artifact_id"), nullable=True)
    museum_id = Column(UUID(as_uuid=True), ForeignKey("museums.museum_id"), nullable=False)
    


