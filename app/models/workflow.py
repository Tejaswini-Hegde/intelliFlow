from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.config.database import Base

class WorkflowModel(Base):
    # 1. Define the actual table name inside PostgreSQL
    __tablename__ = "workflows"

    # 2. Define the structural columns
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="draft")
    is_active = Column(Boolean, default=True)

    # 3. Define automatic timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
