from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class ConditionReportCreate(BaseModel):
    artifact_id: UUID
    report_date: datetime
    condition_rating: Optional[float] = None
    notes: Optional[str] = None


class ConditionReportRead(ConditionReportCreate):
    artifact_id: UUID
    report_date: datetime
    condition_rating: Optional[float] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True