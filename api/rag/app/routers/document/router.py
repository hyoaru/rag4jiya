from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from loguru import logger

from app.services.document_vector_collection import DocumentVectorCollectionService
from .models import DocumentUploadResponse

router = APIRouter()


@router.post(
    "/documents",
    status_code=status.HTTP_201_CREATED,
    response_model=DocumentUploadResponse,
)
async def upload_document(
    document: Annotated[UploadFile, File()],
    document_id: Annotated[str, Form()],
    document_title: Annotated[str, Form()],
    document_type: Annotated[str, Form()],
    user_id: Annotated[str, Form()],
):
    log_context = {
        "user_id": user_id,
        "document_title": document_title,
        "document_type": document_type,
        "file_name": document.filename,
        "file_size_bytes": document.size,
    }

    logger.bind(**log_context).info("Received upload request")

    if document.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {document.content_type}. Only PDF files are allowed.",
        )

    document_vector_collection_service = DocumentVectorCollectionService()

    try:
        await document_vector_collection_service.upload_document(
            user_id=user_id,
            document=document,
            document_id=document_id,
            document_title=document_title,
            document_type=document_type,
        )

        return DocumentUploadResponse(
            status="success",
            message="Document uploaded and processed successfully",
        )

    except ValueError as e:
        logger.bind(**log_context).warning(f"Upload failed: {e}")
        raise HTTPException(status_code=422, detail=str(e))

    except RuntimeError as e:
        logger.bind(**log_context).error(f"Embedding/vector DB error: {e}")
        raise HTTPException(status_code=502, detail=str(e))

    except Exception as e:
        logger.bind(**log_context).exception(f"Unexpected error during upload: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
