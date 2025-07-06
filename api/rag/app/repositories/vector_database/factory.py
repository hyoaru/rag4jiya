from .interface import VectorDatabaseRepositoryABC
from .qdrant import QdrantVectorDatabaseRepository


class VectorDatabaseRepositoryFactory:
    @classmethod
    def create(cls, name: str) -> VectorDatabaseRepositoryABC:
        match name:
            case "QDRANT":
                return QdrantVectorDatabaseRepository()
            case _:
                raise ValueError(f"Unknown vector database name: {name}")
