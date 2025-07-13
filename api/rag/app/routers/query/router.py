from fastapi import APIRouter

from app.services.clinical_insight_agent.service import ClinicalInsightAgentService
from app.utilities.custom_logger import CustomLogger

from .models import QueryRequest

router = APIRouter()
logger = CustomLogger.get_instance()


@router.post("/query")
async def query(request: QueryRequest):
    log_context = {"user_id": request.user_id, "query": request.query}

    logger.info("Query request received", extra=log_context)

    return await ClinicalInsightAgentService().run(
        query=request.query, user_id=request.user_id
    )
