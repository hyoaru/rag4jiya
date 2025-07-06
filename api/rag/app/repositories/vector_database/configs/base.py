from pathlib import Path
from typing import Dict, Literal, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

root_directory = Path(__file__).parents[4]
env_file = root_directory / ".env"


class BaseVectorDatabaseConfig(BaseSettings):
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API key")
    OPENAI_EMBEDDING_MODEL: Optional[Literal["text-embedding-3-small"]] = Field(
        default=None,
        description="OpenAI embedding model name",
    )

    OPENAI_EMBEDDING_SIZES: Dict[str, int] = {
        "text-embedding-ada-002": 1536,
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
    }

    @property
    def OPENAI_EMBEDDING_SIZE(self) -> int:
        if not self.OPENAI_EMBEDDING_MODEL:
            raise ValueError(
                "OPENAI_EMBEDDING_MODEL must be set to get the embedding size."
            )
        return self.OPENAI_EMBEDDING_SIZES[self.OPENAI_EMBEDDING_MODEL]

    @field_validator("OPENAI_API_KEY", "OPENAI_EMBEDDING_MODEL", mode="after")
    def check_required(cls, v, info):
        if not v:
            raise ValueError(
                f"{info.field_name} must be set in environment or passed explicitly."
            )
        return v

    class Config:
        env_file = env_file
        env_file_encoding = "utf-8"
