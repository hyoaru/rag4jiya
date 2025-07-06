import time
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from .api.routers.health.router import router as health_router


def create_app():
    load_dotenv()

    app = FastAPI(title="Rag4Jiya RAG API", docs_url="/api/docs")
    logger.add(
        "./logs/app.log",
        rotation="1 day",
        retention="7 days",
        level="INFO",
        format="[{time:YYYY-MM-DD HH:mm:ss}] [{level}] - {message}",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s"
        )
        return response

    app.include_router(health_router, prefix="/api")

    return app
