from typing import List
from pydantic import BaseModel

from app.common.models.document_type import DocumentType


class QueryRequest(BaseModel):
    user_id: str
    query: str
    sources: List[DocumentType]
