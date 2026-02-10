import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from src.base import Base

class Museum(Base):
    __tablename__ = 'museums'
    museum_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    contact_email = Column(String, nullable=False)