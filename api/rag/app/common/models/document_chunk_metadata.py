from pydantic import BaseModel

from app.common.models import DocumentType


class DocumentChunkMetadata(BaseModel):
    user_id: str
    document_id: str
    document_type: DocumentType
    document_title: str
    heading: str
    content: str
    page_number: int
