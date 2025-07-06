from pydantic import BaseModel, Field
from typing import Literal


class HealthResponseBody(BaseModel):
    status: Literal["ok", "degraded", "down"] = Field(
        ..., description="ok | degraded | down"
    )
    redis: Literal["ok", "unreachable"] = Field(..., description="ok | unreachable")
    chromadb: Literal["ok", "unreachable"] = Field(..., description="ok | unreachable")
