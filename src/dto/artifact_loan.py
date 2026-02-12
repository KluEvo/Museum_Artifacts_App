from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class ArtifactLoanCreate(BaseModel):

    artifact_id: UUID
    loan_id: UUID
    display_requirements: Optional[str] = None
    return_condition_required: Optional[str] = None


class ArtifactLoanRead(ArtifactLoanCreate):

    artifact_id: UUID
    loan_id: UUID
    display_requirements: Optional[str] = None
    return_condition_required: Optional[str] = None

    class Config:
        from_attributes = True
