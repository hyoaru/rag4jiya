from typing import List
from .interface import TextEmbedderRepositoryABC


class OpenAiTextEmbedderRepository(TextEmbedderRepositoryABC):
    def __init__(self, *args, **kwargs):
        pass

    async def embed(self, text: str) -> List[float]:
        pass

    async def embed_batch(self, text: List[str]) -> List[float]:
        pass
