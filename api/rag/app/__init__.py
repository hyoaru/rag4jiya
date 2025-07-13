import logging
import time

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.custom_logging import setup_logging

from .routers.document.router import router as document_router
from .routers.health.router import router as health_router
from .routers.query.router import router as query_router


def create_app():
    load_dotenv()
    setup_logging()

    app = FastAPI(
        title="Rag4Jiya RAG API",
        docs_url="/api/docs",
        redocs="/api/redoc",
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
        logging.info(
            f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s"
        )
        return response

    app.include_router(health_router, prefix="/api")
    app.include_router(query_router, prefix="/api")
    app.include_router(document_router, prefix="/api")

    return app
