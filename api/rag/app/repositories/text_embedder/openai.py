from typing import List, cast
from openai import AsyncOpenAI
from app.common.configs.environment import EnvironmentConfig
from .interface import TextEmbedderRepositoryABC


class OpenAiTextEmbedderRepository(TextEmbedderRepositoryABC):
    def __init__(self):
        self._environment_config = EnvironmentConfig()
        self._client = AsyncOpenAI(api_key=self._environment_config.OPENAI_API_KEY)
        self._embedding_model = self._environment_config.OPENAI_EMBEDDING_MODEL

    async def embed(self, text: str) -> List[float]:
        response = await self._client.embeddings.create(
            model=cast(str, self._embedding_model),
            input=text,
        )

        return response.data[0].embedding

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        response = await self._client.embeddings.create(
            model=cast(str, self._embedding_model),
            input=texts,
        )

        return [item.embedding for item in response.data]
