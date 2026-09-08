from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.workflow import WorkflowResponse
from app.repositories.workflow import workflow_repo
from app.services.pipeline import pipeline_service

router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"]
)

@router.post("/", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
def upload_and_process_document(
        document_id: str = Form(..., description="Unique structural key identifier for this document"),
        file: UploadFile = Form(..., description="The multi-page PDF or text file payload"),
        db: Session = Depends(get_db)
):
    """
    Executes an end-to-end processing pipeline on a real uploaded document.
    Saves metadata to PostgreSQL, handles local storage, extracts text, and appends AI layers.
    """
    # 1. Prevent duplicate IDs from crashing the pipeline early
    existing_record = workflow_repo.get_workflow(db=db, workflow_id=document_id)
    if existing_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A document pipeline record with ID '{document_id}' already exists."
        )

    try:
        # 2. Trigger our orchestrator to handle the full file lifecycle process
        completed_record = pipeline_service.process_document_pipeline(
            file=file,
            custom_id=document_id,
            db=db
        )
        return completed_record
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pipeline processing failed: {str(e)}"
        )

@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_pipeline_results(workflow_id: str, db: Session = Depends(get_db)):
    """
    Step 10 of Plan: Exposes a GET API allowing users to fetch structural AI processing outputs.
    """
    db_workflow = workflow_repo.get_workflow(db=db, workflow_id=workflow_id)
    if not db_workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document workflow record '{workflow_id}' not found."
        )
    return db_workflow
