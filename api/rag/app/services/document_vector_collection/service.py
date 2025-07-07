from fastapi import UploadFile
from app.repositories.text_embedder import (
    TextEmbedderRepositoryABC,
    TextEmbedderRepositoryFactory,
)
from app.repositories.vector_database import (
    VectorDatabaseRepositoryABC,
    VectorDatabaseRepositoryFactory,
)

from .interface import DocumentVectorCollectionServiceABC


class DocumentVectorCollectionService(DocumentVectorCollectionServiceABC):
    def __init__(self):
        self._collection_name = "documents"
        self._text_embedder_repository: TextEmbedderRepositoryABC = (
            TextEmbedderRepositoryFactory.create("OPENAI")
        )
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
        document_type: str,
    ):
        await self._vector_database_repository.upsert_vectors(
            collection=self._collection_name,
            vectors=[embeddings],
            metadatas=None,
        )
        pass
