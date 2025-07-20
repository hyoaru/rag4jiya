from fastapi import UploadFile

from app.common.models import DocumentType, DocumentChunkMetadata
from app.repositories.vector_database import (
    VectorDatabaseRepositoryABC,
    VectorDatabaseRepositoryFactory,
)
from app.utilities.docling_document_processor import DoclingDocumentProcessorUtility
from app.utilities.text_embedder import TextEmbedderUtilityFactory


class DocumentVectorCollectionService:
    def __init__(self):
        # Initialize the vector DB repository for the "documents" collection
        self._collection_name = "documents"
        self._text_embedder = TextEmbedderUtilityFactory.create("openai")
        self._vector_database_repository: VectorDatabaseRepositoryABC = (
            VectorDatabaseRepositoryFactory.create("QDRANT")
        )

    async def apply_migrations(self):
        # Create the collection if it doesn't exist
        await self._vector_database_repository.create_collection(
            name=self._collection_name
        )

    async def search(self, user_id: str, document_type: DocumentType, text: str):
        # Embed the input query text
        query_vector = await self._text_embedder.embed(text)

        # Search for similar document chunks
        result = await self._vector_database_repository.search_collection(
            collection=self._collection_name,
            query_vector=query_vector,
            metadatas={"user_id": user_id, "document_type": document_type.value},
        )

    async def upload_document(
        self,
        user_id: str,
        document: UploadFile,
        document_id: str,
        document_title: str,
        document_type: DocumentType,
    ):
        # Convert file into a structured docling document
        docling_document = await DoclingDocumentProcessorUtility.to_docling(document)

        # Break the document into chunks (per heading/page)
        chunks = DoclingDocumentProcessorUtility.chunk_to_lists(docling_document)

        # Generate embeddings for each chunk
        text_embeddings = await self._text_embedder.embed_batch(chunks.texts)

        # Prepare metadata for each chunk
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

        # Upsert all vectors with metadata into the vector database
        await self._vector_database_repository.upsert_vectors(
            collection=self._collection_name,
            vectors=text_embeddings,
            metadatas=metadatas,
        )
