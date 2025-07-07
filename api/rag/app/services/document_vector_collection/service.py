from fastapi import UploadFile

from app.common.models.document_chunk_embedded import DocumentChunkEmbedded
from app.repositories.vector_database import (
    VectorDatabaseRepositoryABC,
    VectorDatabaseRepositoryFactory,
)
from app.utilities.docling_document_processor.utility import (
    DoclingDocumentProcessorUtility,
)
from app.utilities.openai_text_embedder.utility import OpenAiTextEmbedderUtility


class DocumentVectorCollectionService:
    def __init__(self):
        self._collection_name = "documents"
        self._vector_database_repository: VectorDatabaseRepositoryABC = (
            VectorDatabaseRepositoryFactory.create("QDRANT")
        )

    async def apply_migrations(self):
        await self._vector_database_repository.create_collection(
            name=self._collection_name
        )

    async def similarity_search_across_documents(self, user_id: str, text: str):
        pass

    async def upload_document(
        self,
        user_id: str,
        document: UploadFile,
        document_title: str,
        document_type: str,
    ):
        # 1. Convert the file into a docling document
        docling_document = await DoclingDocumentProcessorUtility.to_docling(document)

        # 2. Chunk the document
        document_chunks = DoclingDocumentProcessorUtility.chunk(docling_document)

        # 3. Embed the enriched text from the chunks
        texts = [chunk.text for chunk in document_chunks]
        embedded_texts = await OpenAiTextEmbedderUtility().embed_batch(texts)
        embedded_document_chunks = [
            DocumentChunkEmbedded(**chunk.model_dump(), text_embeddings=text_embeddings)
            for chunk, text_embeddings in zip(document_chunks, embedded_texts)
        ]

        return embedded_document_chunks
