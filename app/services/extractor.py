import os
from pypdf import PdfReader

class TextExtractorService:
    def extract_text(self, file_path: str) -> str:
        """
        Reads a local file path, detects the format, and extracts all text content.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Target file not found at: {file_path}")

        _, ext = os.path.splitext(file_path.lower())

        if ext == ".txt":
            return self._extract_txt(file_path)
        elif ext == ".pdf":
            return self._extract_pdf(file_path)
        else:
            raise ValueError(f"Unsupported extraction format: {ext}")

    def _extract_txt(self, file_path: str) -> str:
        """Extracts text from plain text files."""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _extract_pdf(self, file_path: str) -> str:
        """Extracts text from multi-page PDF documents."""
        reader = PdfReader(file_path)
        extracted_pages = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_pages.append(text)

        return "\n".join(extracted_pages)

# Create a single reusable extractor manager
extractor_service = TextExtractorService()
