import uuid
from typing import Dict, List, Union, Optional

from loguru import logger
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.common.configs.environment import EnvironmentConfig
from .interface import VectorDatabaseRepositoryABC


class QdrantVectorDatabaseRepository(VectorDatabaseRepositoryABC):
    def __init__(self):
        self._environment_config = EnvironmentConfig()

        self._vectors_config = VectorParams(
            size=self._environment_config.OPENAI_EMBEDDING_SIZE,
            distance=Distance.COSINE,
        )

        self._client = AsyncQdrantClient(
            url=self._environment_config.QDRANT_BASE_URL,
        )

    async def create_collection(self, name: str):
        is_created = await self._client.create_collection(
            collection_name=name,
            vectors_config=self._vectors_config,
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
        vectors: List[List[float]],
        metadatas: List[Dict[str, Union[str, int, float, bool, None]]],
        ids: Optional[List[str] | List[None]] = None,
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

        try:
            await self._client.upsert(collection_name=collection, points=points)
        except Exception as e:
            raise ValueError(
                f"Failed to upsert vectors into collection `{collection}`: {e}"
            ) from e
