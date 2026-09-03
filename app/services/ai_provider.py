from abc import ABC, abstractmethod
from typing import Dict, Any

class AIProvider(ABC):
    """
    Abstract Base Class that enforces a strict contract for all AI engines.
    Both your Local provider and future AWS Bedrock provider must follow this.
    """
    @abstractmethod
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Reads raw string text and returns standard structured insights."""
        pass


class LocalAIProvider(AIProvider):
    """
    Your free local mock implementation. It simulates processing the text
    and returns perfectly structured data without calling any paid APIs.
    """
    def analyze_text(self, text: str) -> Dict[str, Any]:
        # Clean the text sample length for preview safety
        preview_text = text[:60].replace("\n", " ") + "..." if len(text) > 60 else text

        # 1. Simulating classification logic based on text patterns
        lower_text = text.lower()
        if "invoice" in lower_text or "total due" in lower_text:
            doc_type = "Invoice"
        elif "report" in lower_text or "revenue" in lower_text or "quarter" in lower_text:
            doc_type = "Financial Report"
        elif "contract" in lower_text or "agreement" in lower_text:
            doc_type = "Contract"
        else:
            doc_type = "General Document"

        # 2. Constructing the standardized AI output payload structure
        return {
            "summary": f"Automatically processed text document. Preview: '{preview_text}'",
            "classification": doc_type,
            "key_insights": [
                f"Successfully parsed input containing {len(text)} raw characters.",
                f"Identified primary structural layout markers matching a {doc_type}.",
                "Extracted context data and queued for archival pipeline storage."
            ]
        }

# Instantiate your free active local provider for the system to use right now
ai_provider = LocalAIProvider()
