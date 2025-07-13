from typing import List, cast

from openai import AsyncOpenAI
from app.common.configs.environment import EnvironmentConfig
from .interface import TextEmbedderUtilityABC


class OpenAiTextEmbedderUtility(TextEmbedderUtilityABC):
    """Async helper that turns text (or a batch of texts) into OpenAI embeddings."""

    def __init__(self) -> None:
        environment_config = EnvironmentConfig()
        self._client = AsyncOpenAI(api_key=environment_config.OPENAI_API_KEY)
        self._model = environment_config.OPENAI_EMBEDDING_MODEL

    async def embed(self, text: str) -> List[float]:
        """Return a single embedding vector for `text`."""
        try:
            resp = await self._client.embeddings.create(
                model=cast(str, self._model),
                input=text,
            )
            return resp.data[0].embedding
        except Exception as e:
            raise ValueError(f"Failed to embed text {text!r}") from e

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple strings in one API call."""
        try:
            resp = await self._client.embeddings.create(
                model=cast(str, self._model),
                input=texts,
            )
            return [item.embedding for item in resp.data]
        except Exception as e:
            raise ValueError("Failed to embed batch") from e
