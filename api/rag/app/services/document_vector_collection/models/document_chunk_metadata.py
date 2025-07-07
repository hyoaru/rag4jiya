from pydantic import BaseModel


class DocumentChunkMetadata(BaseModel):
    user_id: str
    document_id: str
    document_type: str
    document_title: str
    heading: str
    content: str
    page_number: int
