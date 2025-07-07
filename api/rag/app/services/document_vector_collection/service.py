from fastapi import UploadFile

from app.repositories.vector_database import (
    VectorDatabaseRepositoryABC,
    VectorDatabaseRepositoryFactory,
)
from app.services.document_vector_collection.models.document_chunk_metadata import (
    DocumentChunkMetadata,
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
        document_id: str,
        document_title: str,
        document_type: str,
    ):
        # 1. Convert the file into a docling document
        docling_document = await DoclingDocumentProcessorUtility.to_docling(document)

        # 2. Chunk the document to lists for vector database to consume
        chunks = DoclingDocumentProcessorUtility.chunk_to_lists(docling_document)

        # 3. Embed the enriched text from the chunks
        text_embeddings = await OpenAiTextEmbedderUtility().embed_batch(chunks.texts)
        metadatas = [
            DocumentChunkMetadata(
                user_id=user_id,
                document_id=document_id,
                document_type=document_type,
                document_title=document_title,
                heading=heading,
                content=text,
                page_number=page_number,
            ).model_dump()
            for text, page_number, heading in zip(
                chunks.texts, chunks.page_numbers, chunks.headings
            )
        ]

        # 4. Upload to Qdrant
        await self._vector_database_repository.upsert_vectors(
            collection=self._collection_name,
            vectors=text_embeddings,
            metadatas=metadatas,
        )
