import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from src.base import Base

class Artifact(Base):
    __tablename__ = "artifacts"
