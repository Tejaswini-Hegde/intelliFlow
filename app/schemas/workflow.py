from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 1. Rules for data coming IN (when creating a new workflow)
class WorkflowCreate(BaseModel):
    id: str = Field(..., description="Unique identifier for the workflow")
    name: str = Field(..., min_length=1, max_length=100, description="The name of the automation workflow")
    description: Optional[str] = Field(None, max_length=500)

# 2. Rules for data going OUT (what we return to the user's browser)
class WorkflowResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: str
    is_active: bool
    created_at: datetime

    # Tells Pydantic to cleanly read data from database rows
    model_config = {"from_attributes": True}
