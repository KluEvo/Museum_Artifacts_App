from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from pydantic.config import ConfigDict

class ArtifactLoanCreate(BaseModel):

    artifact_id: UUID
    loan_id: UUID
    display_requirements: Optional[str] = None
    return_condition_required: Optional[str] = None


class ArtifactLoanRead(ArtifactLoanCreate):

    model_config = ConfigDict(from_attributes = True)
    artifact_id: UUID
    loan_id: UUID
    display_requirements: Optional[str] = None
    return_condition_required: Optional[str] = None

