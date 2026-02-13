from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from pydantic.config import ConfigDict

class ConditionReportCreate(BaseModel):
    artifact_id: UUID
    report_date: datetime
    condition_rating: Optional[float] = None
    notes: Optional[str] = None


class ConditionReportRead(ConditionReportCreate):

    model_config = ConfigDict(from_attributes = True)
    artifact_id: UUID
    report_date: datetime
    condition_rating: Optional[float] = None
    notes: Optional[str] = None