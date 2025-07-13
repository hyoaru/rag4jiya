from pydantic import BaseModel

from app.services.document_vector_collection.service import (
    DocumentVectorCollectionService,
)


class AgentDependencies(BaseModel):
    query: str
    user_id: str
    document_vector_collection_service: DocumentVectorCollectionService

    class Config:
        arbitrary_types_allowed = True
