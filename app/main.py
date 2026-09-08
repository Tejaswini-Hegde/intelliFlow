from fastapi import FastAPI

from app.config.settings import settings
from app.services.workflow import workflow_service
from app.routes.workflow import router as workflow_router

# Initialize the FastAPI application using our configuration settings
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# ⭐ Wire the endpoints container into the primary application engine
app.include_router(workflow_router)

@app.get("/")
def read_root():
    """
    The landing endpoint for the API. Returns basic project info.
    """
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "message": "Welcome to IntelliFlow Backend"
    }

@app.get("/health")
def health_check():
    """
    A dedicated health check endpoint that asks our workflow service for its status.
    """
    return workflow_service.get_status()
