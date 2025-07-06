import uuid
from typing import Dict, List, Union, Optional, cast

from loguru import logger
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from .configs import BaseVectorDatabaseConfig, QdrantVectorDatabaseConfig
from .interface import VectorDatabaseRepositoryABC


class QdrantVectorDatabaseRepository(VectorDatabaseRepositoryABC):
    def __init__(self):
        self._base_config = BaseVectorDatabaseConfig()
        self._config = QdrantVectorDatabaseConfig()

        self._vectors_config = VectorParams(
            size=self._base_config.OPENAI_EMBEDDING_SIZE,
            distance=Distance.COSINE,
        )

    def async_init(self):
        self._client = AsyncQdrantClient(url=self._config.BASE_URL)

    async def create_collection(self, name: str):
        is_created = await self._client.create_collection(
            collection_name=name,
            vectors_config=self._vectors_config,
            exist_ok=True,
        )

        if not is_created:
            raise ValueError(f"Failed to create collection: {name}")
        else:
            logger.info(f"Created collection: {name}")

    async def search_collection(
        self,
        name: str,
        query_vector: List[float],
        top_n: int = 3,
    ):
        return await self._client.search(
            collection_name=name,
            query_vector=query_vector,
            top=top_n,
        )

    async def upsert_vectors(
        self,
        collection: str,
        ids: Optional[List[str] | List[None]],
        vectors: List[List[float]],
        metadatas: List[Dict[str, Union[str, int, float, bool, None]]],
    ):
        if ids and len(ids) != len(vectors):
            raise ValueError(
                f"Length of ids ({len(ids)}) does not match length of vectors ({len(vectors)})"
            )

        ids = ids or [None] * len(vectors)

        points = [
            PointStruct(
                id=provided_id if provided_id else str(uuid.uuid4()),
                vector=vector,
                payload=metadata,
            )
            for provided_id, vector, metadata in zip(ids, vectors, metadatas)
        ]

        await self._client.upsert(collection_name=collection, points=points)
