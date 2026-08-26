from sqlalchemy.orm import Session
from app.models.workflow import WorkflowModel
from app.schemas.workflow import WorkflowCreate

class WorkflowRepository:

    def create_workflow(self, db: Session, workflow_in: WorkflowCreate) -> WorkflowModel:
        """
        Takes verified schema data and saves it permanently as a row in PostgreSQL.
        """
        # 1. Convert the incoming schema data into a database Model object
        db_workflow = WorkflowModel(
            id=workflow_in.id,
            name=workflow_in.name,
            description=workflow_in.description,
            status="draft"  # All workflows start as a draft
        )

        # 2. Tell the database connection to prepare this row
        db.add(db_workflow)

        # 3. Permanently write the transaction to disk
        db.commit()

        # 4. Refresh our Python object with any database-generated fields (like timestamps)
        db.refresh(db_workflow)

        return db_workflow

# Instantiate a single reusable repository manager
workflow_repo = WorkflowRepository()
