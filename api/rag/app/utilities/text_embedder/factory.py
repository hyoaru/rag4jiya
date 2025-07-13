from app.utilities.text_embedder.interface import TextEmbedderUtilityABC
from app.utilities.text_embedder.openai import OpenAiTextEmbedderUtility


class TextEmbedderUtilityFactory:
    @staticmethod
    def create(name: str) -> TextEmbedderUtilityABC:
        match name:
            case "openai":
                return OpenAiTextEmbedderUtility()
            case _:
                raise ValueError(f"Unknown text embedder name: {name}")
