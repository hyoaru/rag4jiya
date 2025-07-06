from abc import ABC, abstractmethod
from typing import List


class TextEmbedderRepositoryABC(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        pass

    @abstractmethod
    async def embed_batch(self, text: List[str]) -> List[float]:
        pass
