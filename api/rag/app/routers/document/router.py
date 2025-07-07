from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from loguru import logger

from app.services.document_vector_collection import DocumentVectorCollectionService

router = APIRouter()


@router.post("/documents")
async def upload_document(
    document: Annotated[UploadFile, File()],
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

    return await document_vector_collection_service.upload_document(
        user_id=user_id,
        document=document,
        document_title=document_title,
        document_type=document_type,
    )
