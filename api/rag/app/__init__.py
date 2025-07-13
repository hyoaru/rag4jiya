import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.utilities.custom_logger import CustomLogger

from .routers.document.router import router as document_router
from .routers.health.router import router as health_router
from .routers.query.router import router as query_router


def create_app():
    CustomLogger.setup_logging()
    logger = CustomLogger.get_instance()

    app = FastAPI(
        title="Rag4Jiya RAG API",
        docs_url="/docs",
        redoc_url="/redoc",
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
    app.include_router(query_router, prefix="/api")
    app.include_router(document_router, prefix="/api")

    return app
