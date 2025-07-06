from fastapi import APIRouter
from .models import HealthResponseBody

router = APIRouter()


@router.get("/health", response_model=HealthResponseBody)
async def health():
    return HealthResponseBody(
        status="ok",
        redis="ok",
        chromadb="ok",
    )
