from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class ArtifactCreate(BaseModel):

    accession_number: str
    name: str
    discovery_date: Optional[datetime] = None
    estimated_value: Optional[int] = None 
    
    parent_artifact: Optional[UUID] = None
    museum_id: UUID 


class ArtifactRead(ArtifactCreate):

    artifact_id: UUID
    accession_number: str
    name: str
    discovery_date: Optional[datetime] = None
    estimated_value: Optional[int] = None 
    parent_artifact: Optional[UUID] = None
    museum_id: UUID 

    class Config:
        from_attributes = True

