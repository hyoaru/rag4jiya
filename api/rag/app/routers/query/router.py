from fastapi import APIRouter
from .models import QueryRequest
from app.services.document_vector_collection import DocumentVectorCollectionService

router = APIRouter()


@router.post("/query")
async def query(request: QueryRequest):
    document_vector_collection_service = DocumentVectorCollectionService()
    embeddings = (
        await document_vector_collection_service.similarity_search_across_documents(
            user_id="user_id",
            text=request.query,
        )
    )

    return embeddings
