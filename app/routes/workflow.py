from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.workflow import WorkflowCreate, WorkflowResponse
from app.repositories.workflow import workflow_repo

router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"]
)

@router.post("/", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
def create_new_document_workflow(workflow_in: WorkflowCreate, db: Session = Depends(get_db)):
    """
    Step 5 of Plan: Receives validation data and saves metadata to PostgreSQL with status='uploaded'.
    """
    try:
        new_workflow = workflow_repo.create_workflow(db=db, workflow_in=workflow_in)
        return new_workflow
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to record pipeline: {str(e)}"
        )

@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_pipeline_results(workflow_id: str, db: Session = Depends(get_db)):
    """
    Step 10 of Plan: User triggers this GET endpoint to fetch the completed AI results.
    """
    # Note: We will implement the get_by_id logic in our repository next
    db_workflow = workflow_repo.get_workflow(db=db, workflow_id=workflow_id)
    if not db_workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document workflow record not found"
        )
    return db_workflow
