from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class MuseumCreate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    contact_email: Optional[str] = None


class MuseumRead(MuseumCreate):
    museum_id: UUID
    name: Optional[str] = None
    location: Optional[str] = None
    contact_email: Optional[str] = None

    class Config:
        from_attributes = True
