from typing import Dict, List

from pydantic import BaseModel

from app.common.models.document_chunk_metadata import DocumentChunkMetadata
from app.common.models.document_type import DocumentType


class AgentDependencies(BaseModel):
    query: str
    user_id: str
    references: Dict[DocumentType, List[DocumentChunkMetadata]]
