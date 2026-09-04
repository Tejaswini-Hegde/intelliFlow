from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.schemas.workflow import WorkflowCreate
from app.repositories.workflow import workflow_repo
from app.services.storage import storage_service
from app.services.extractor import extractor_service
from app.services.ai_provider import ai_provider

class DocumentPipelineService:
    def process_document_pipeline(self, file: UploadFile, custom_id: str, db: Session):
        """
        Executes the full Intelligent Document Processing lifecycle.
        """
        # Step 1: Create initial tracking record in PostgreSQL (Status = uploaded)
        workflow_in = WorkflowCreate(
            id=custom_id,
            name=file.filename if file.filename else "unnamed_document",
            description="Document uploaded to the automated IDP pipeline."
        )
        db_record = workflow_repo.create_workflow(db=db, workflow_in=workflow_in)

        try:
            # Step 2: Save the physical binary file to Local Disk Storage (Mirrors S3)
            local_file_path = storage_service.save_file(file=file, custom_id=custom_id)

            # Step 3: Transition database state to 'processing'
            db_record.status = "processing"
            db.commit()

            # Step 4: Extract raw string content from the file
            extracted_text = extractor_service.extract_text(local_file_path)
            db_record.extracted_text = extracted_text

            # Step 5: Route extracted text to the AI Layer for insights
            ai_results = ai_provider.analyze_text(extracted_text)

            # Step 6: Map AI insights to model and mark pipeline as 'completed'
            db_record.summary = ai_results["summary"]
            db_record.classification = ai_results["classification"]
            db_record.key_insights = ai_results["key_insights"]
            db_record.status = "completed"

            # Commit all final updates permanently to PostgreSQL
            db.commit()
            db.refresh(db_record)
            return db_record

        except Exception as e:
            # Fallback Safety: If any phase fails, mark the tracking record as failed
            db_record.status = "failed"
            db.commit()
            raise RuntimeError(f"Pipeline execution aborted: {str(e)}")

# Create a single reusable orchestrator manager
pipeline_service = DocumentPipelineService()
