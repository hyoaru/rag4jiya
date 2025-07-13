import uuid
from itertools import repeat
from typing import List, Optional

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Condition,
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from app.common.configs.environment import EnvironmentConfig

from .interface import VectorDatabaseRepositoryABC
from .models import VectorSearchResult


class QdrantVectorDatabaseRepository(VectorDatabaseRepositoryABC):
    def __init__(self):
        # Initialize vector database connection and vector configuration
        self._environment_config = EnvironmentConfig()
        self._vectors_config = VectorParams(
            size=self._environment_config.OPENAI_EMBEDDING_SIZE,
            distance=Distance.COSINE,
        )
        self._client = AsyncQdrantClient(
            url=self._environment_config.QDRANT_BASE_URL,
        )

    async def create_collection(self, name: str):
        # Create a new Qdrant collection if it doesn't already exist
        is_created = await self._client.create_collection(
            collection_name=name,
            vectors_config=self._vectors_config,
        )
        if not is_created:
            raise ValueError(f"Failed to create collection: {name}")

    async def search_collection(
        self,
        collection,
        query_vector,
        metadatas=None,
        top_n=3,
    ):
        # Optional metadata filter construction
        query_filter: Optional[Filter] = None
        if metadatas:
            conditions: List[Condition] = [
                FieldCondition(key=k, match=MatchValue(value=v))
                for k, v in metadatas.items()
                if isinstance(v, (str, int, bool))
            ]
            if conditions:
                query_filter = Filter(must=conditions)

        # Perform vector similarity search
        search_results = await self._client.search(
            collection_name=collection,
            query_vector=query_vector,
            limit=top_n,
            with_payload=True,
            query_filter=query_filter,
        )

        # Map Qdrant results to domain DTOs
        processed_search_results = []
        for result in search_results:
            result_map = result.model_dump()
            processed_search_results.append(
                VectorSearchResult(
                    id=result_map["id"],
                    score=result_map["score"],
                    content=result_map["payload"]["content"],
                    metadata={
                        k: v for k, v in result_map["payload"].items() if k != "content"
                    },
                )
            )
        return processed_search_results

    async def upsert_vectors(self, collection, vectors, metadatas, ids=None):
        # Ensure provided IDs match vector count (if given)
        if ids and len(ids) != len(vectors):
            raise ValueError(
                f"Length of ids ({len(ids)}) does not match length of vectors ({len(vectors)})"
            )

        # Use UUIDs if no IDs provided
        ids = ids or repeat(None, len(vectors))

        # Prepare points for upsert
        points = [
            PointStruct(
                id=provided_id if provided_id else str(uuid.uuid4()),
                vector=vector,
                payload=metadata,
            )
            for provided_id, vector, metadata in zip(ids, vectors, metadatas)
        ]

        # Upsert into Qdrant
        try:
            await self._client.upsert(collection_name=collection, points=points)
        except Exception as e:
            raise ValueError(
                f"Failed to upsert vectors into collection `{collection}`: {e}"
            ) from e
