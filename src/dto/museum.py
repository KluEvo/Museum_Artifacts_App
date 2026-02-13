from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from pydantic.config import ConfigDict

class MuseumCreate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    contact_email: Optional[str] = None


class MuseumRead(MuseumCreate):

    model_config = ConfigDict(from_attributes = True)
    museum_id: UUID
    name: Optional[str] = None
    location: Optional[str] = None
    contact_email: Optional[str] = None
