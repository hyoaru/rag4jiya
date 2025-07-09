from fastapi import APIRouter
from loguru import logger

from app.services.document_vector_collection import DocumentVectorCollectionService

from .models import QueryRequest

router = APIRouter()


@router.post("/query")
async def query(request: QueryRequest):
    log_context = {
        "user_id": request.user_id,
        "query": request.query,
    }

    logger.bind(**log_context).info("Received query request")

    document_vector_collection_service = DocumentVectorCollectionService()

    similar_documents = (
        await document_vector_collection_service.similarity_search_across_documents(
            user_id=request.user_id,
            text=request.query,
        )
    )

    return similar_documents
