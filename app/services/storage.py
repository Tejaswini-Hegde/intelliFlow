import os
import shutil
from fastapi import UploadFile
from app.config.settings import settings

class LocalStorageService:
    def __init__(self):
        # Ensure the storage directory exists on your machine immediately
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    def save_file(self, file: UploadFile, custom_id: str) -> str:
        """
        Saves an incoming FastAPI UploadFile stream directly to local disk.
        Returns the absolute local file path where it is stored.
        """
        # Extract file extension (e.g., '.pdf') safely
        _, ext = os.path.splitext(file.filename) if file.filename else ("", "")

        # Unique name using our pipeline identifier to prevent overwriting files
        unique_filename = f"{custom_id}{ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

        # Stream file contents to the local disk block-by-block
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path

# Create a single reusable storage utility manager
storage_service = LocalStorageService()
