from pydantic import BaseModel, Field


class DocumentUploadResponse(BaseModel):
    status: str = Field(..., description="Status of the document upload")
    message: str = Field(..., description="Message of the document upload")
