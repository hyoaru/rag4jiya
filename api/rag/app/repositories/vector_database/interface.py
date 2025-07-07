from abc import ABC, abstractmethod
from typing import List, Any, Dict, Union, Optional


class VectorDatabaseRepositoryABC(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def search_collection(
        self,
        name: str,
        query_vector: List[float],
        top_n: int = 3,
    ) -> Any:
        pass

    @abstractmethod
    async def create_collection(self, name: str):
        pass

    @abstractmethod
    async def upsert_vectors(
        self,
        collection: str,
        vectors: List[List[float]],
        metadatas: List[Dict[str, Union[str, int, float, bool, None]]],
        ids: Optional[List[str] | List[None]] = None,
    ):
        pass
