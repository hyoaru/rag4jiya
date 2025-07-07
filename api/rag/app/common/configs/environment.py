from pathlib import Path
from typing import Dict, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

root_directory = Path(__file__).parents[3]
env_file = root_directory / ".env"


class EnvironmentConfig(BaseSettings):
    QDRANT_BASE_URL: Optional[str] = Field(default=None)
    OPENAI_API_KEY: Optional[str] = Field(default=None)
    OPENAI_EMBEDDING_MODEL: Optional[str] = Field(default=None)

    @property
    def OPENAI_EMBEDDING_SIZE(self) -> int:
        openai_embedding_sizes: Dict[str, int] = {
            "text-embedding-ada-002": 1536,
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
        }

        if not self.OPENAI_EMBEDDING_MODEL:
            raise ValueError(
                "OPENAI_EMBEDDING_MODEL must be set to get the embedding size."
            )

        return openai_embedding_sizes[self.OPENAI_EMBEDDING_MODEL]

    @field_validator(
        "QDRANT_BASE_URL",
        "OPENAI_API_KEY",
        "OPENAI_EMBEDDING_MODEL",
        mode="after",
    )
    def check_required(cls, v, info):
        if not v:
            raise ValueError(
                f"{info.field_name} must be set in environment or passed explicitly."
            )
        return v

    class Config:
        env_file = env_file
        env_file_encoding = "utf-8"
