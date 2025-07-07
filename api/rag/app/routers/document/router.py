from typing import Annotated
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from app.services.document_vector_collection import DocumentVectorCollectionService
from app.services.docling_document_processor import DoclingDocumentProcessor
from loguru import logger

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

    docling_document_processor = DoclingDocumentProcessor()
    docling_document = await docling_document_processor.to_docling_document(document)
    document_chunks = docling_document_processor.chunk(docling_document)
    return document_chunks

    # return {
    #     "filename": document.filename,
    #     "content_type": document.content_type,
    #     "document_title": document_title,
    #     "document_type": document_type,
    #     "user_id": user_id,
    # }
