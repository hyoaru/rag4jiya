from fastapi import APIRouter

from app.services.clinical_insight_agent.service import ClinicalInsightAgentService


from .models import QueryRequest

router = APIRouter()


@router.post("/query")
async def query(request: QueryRequest):
    log_context = {"user_id": request.user_id, "query": request.query}

    return await ClinicalInsightAgentService().run(
        query=request.query, user_id=request.user_id
    )
