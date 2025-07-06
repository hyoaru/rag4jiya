from .interface import TextEmbedderRepositoryABC
from .openai import OpenAiTextEmbedderRepository


class TextEmbedderRepositoryFactory:
    @classmethod
    def create(cls, name: str) -> TextEmbedderRepositoryABC:
        match name:
            case "OPENAI":
                return OpenAiTextEmbedderRepository()
            case _:
                raise ValueError(f"Unknown text embedder name: {name}")
