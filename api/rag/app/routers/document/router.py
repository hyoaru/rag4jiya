from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.common.models import DocumentType
from app.services.document_vector_collection import DocumentVectorCollectionService
from app.utilities.custom_logger import CustomLogger
from .models import DocumentUploadResponse

router = APIRouter()
logger = CustomLogger.get_instance()


@router.post(
    "/documents",
    status_code=status.HTTP_201_CREATED,
    response_model=DocumentUploadResponse,
)
async def upload_document(
    document: Annotated[UploadFile, File()],
    document_id: Annotated[str, Form()],
    document_title: Annotated[str, Form()],
    document_type: Annotated[DocumentType, Form()],
    user_id: Annotated[str, Form()],
):
    log_context = {
        "user_id": user_id,
        "document_title": document_title,
        "document_type": document_type,
        "file_name": document.filename,
        "file_size_bytes": document.size,
    }

    logger.info("Document upload request received", extra=log_context)

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
        logger.warning(f"Upload failed: {e}", extra=log_context)
        raise HTTPException(status_code=422, detail=str(e))

    except RuntimeError as e:
        logger.error(f"Embedding/vector DB error: {e}", extra=log_context)
        raise HTTPException(status_code=502, detail=str(e))

    except Exception as e:
        logger.exception(f"Unexpected error during upload: {e}", extra=log_context)
        raise HTTPException(status_code=500, detail="Internal server error")
