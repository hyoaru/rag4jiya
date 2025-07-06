from abc import ABC, abstractmethod
from chromadb.api.models.AsyncCollection import AsyncCollection


class VectorDatabaseRepositoryABC(ABC):
    @abstractmethod
    async def async_init(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_collection(self, name: str) -> AsyncCollection:
        pass

    @abstractmethod
    async def create_collection(self, name: str) -> AsyncCollection:
        pass

    @abstractmethod
    async def add_vector(
        self,
        collection: str,
        contents: str,
        ids: str,
        metadatas: str,
    ):
        pass
