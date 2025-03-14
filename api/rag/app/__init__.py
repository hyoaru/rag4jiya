import time
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger


def create_app():
    load_dotenv()

    app = FastAPI(docs_url="/")
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

    return app
