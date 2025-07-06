from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

root_directory = Path(__file__).parents[4]
env_file = root_directory / ".env"


class QdrantVectorDatabaseConfig(BaseSettings):
    BASE_URL: Optional[str] = Field(
        default=None, description="Qdrant base url", alias="QDRANT_BASE_URL"
    )

    @field_validator("BASE_URL", mode="after")
    def check_required(cls, v, info):
        if not v:
            raise ValueError(
                f"{info.field_name} must be set in environment or passed explicitly."
            )
        return v

    class Config:
        env_file = env_file
        env_file_encoding = "utf-8"
        populate_by_name = True
