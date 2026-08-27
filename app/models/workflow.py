from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.config.database import Base

class WorkflowModel(Base):
    # 1. Define the actual table name inside PostgreSQL
    __tablename__ = "workflows"

    # 2. Structural Core Meta Columns
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)        # Stores the uploaded filename
    description = Column(String, nullable=True)  # Optional user notes
    status = Column(String, default="uploaded")  # Starts as "uploaded" per your plan
    is_active = Column(Boolean, default=True)

    # 3. ⭐ AI & Text Extraction Columns (Added to match your plan)
    extracted_text = Column(Text, nullable=True)   # Holds the raw text from the PDF
    summary = Column(Text, nullable=True)          # AI Feature 1: Summarization
    classification = Column(String, nullable=True) # AI Feature 2: Document Type
    key_insights = Column(JSON, nullable=True)     # AI Feature 3: Structured JSON Array

    # 4. Define automatic timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
