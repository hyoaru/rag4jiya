from typing import List, cast
from openai import AsyncOpenAI
from app.common.configs.environment import EnvironmentConfig
from .interface import OpenAiTextEmbedderUtilityABC


class OpenAiTextEmbedderUtility(OpenAiTextEmbedderUtilityABC):
    def __init__(self):
        self._environment_config = EnvironmentConfig()
        self._client = AsyncOpenAI(api_key=self._environment_config.OPENAI_API_KEY)
        self._embedding_model = self._environment_config.OPENAI_EMBEDDING_MODEL

    async def embed(self, text: str) -> List[float]:
        try:
            response = await self._client.embeddings.create(
                model=cast(str, self._embedding_model),
                input=text,
            )

            return response.data[0].embedding
        except Exception as e:
            raise ValueError(f"Failed to embed text: {text}. Error: {e}") from e

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        try:
            response = await self._client.embeddings.create(
                model=cast(str, self._embedding_model),
                input=texts,
            )

            return [item.embedding for item in response.data]
        except Exception as e:
            raise ValueError(f"Failed to embed texts: {texts}. Error: {e}") from e
