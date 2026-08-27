from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# 1. Rules for data coming IN (when uploading a document)
class WorkflowCreate(BaseModel):
    id: str = Field(..., description="Unique identifier for the document payload")
    name: str = Field(..., min_length=1, max_length=100, description="The uploaded file name")
    description: Optional[str] = Field(None, max_length=500)

# 2. Rules for data going OUT (what we return to the user's browser / GET API)
class WorkflowResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: str
    is_active: bool

    # ⭐ New AI Outbound Validation Fields
    extracted_text: Optional[str] = None
    summary: Optional[str] = None
    classification: Optional[str] = None
    key_insights: Optional[List[str]] = None  # Validates as a clean array of strings

    created_at: datetime

    # Tells Pydantic to cleanly read data from database rows
    model_config = {"from_attributes": True}
