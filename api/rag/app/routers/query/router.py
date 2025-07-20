import asyncio
from fastapi import APIRouter

from app.common.models.document_type import DocumentType
from app.services.clinical_reference_agent.service import ClinicalReferenceAgentService
from app.services.document_vector_collection.service import (
    DocumentVectorCollectionService,
)
from app.utilities.custom_logger import CustomLogger

from .models import QueryRequest

router = APIRouter()
logger = CustomLogger.get_instance()


@router.post("/query")
async def query(request: QueryRequest):
    log_context = {
        "user_id": request.user_id,
        "query": request.query,
        "sources": request.sources,
    }

    logger.info("Query request received", extra=log_context)

    # Fetch the references by source
    document_collection_service = DocumentVectorCollectionService()
    tasks = [
        document_collection_service.search(request.user_id, source, request.query)
        for source in request.sources
    ]
    results = await asyncio.gather(*tasks)
    references_by_source = {
        source: references for source, references in zip(request.sources, results)
    }

    # Augment the results
    agent_response = await ClinicalReferenceAgentService().run(
        query=request.query,
        user_id=request.user_id,
        references=references_by_source,
    )
