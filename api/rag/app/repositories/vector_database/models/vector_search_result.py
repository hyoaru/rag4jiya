from typing import Dict, Union

from pydantic import BaseModel


class VectorSearchResult(BaseModel):
    id: str
    score: float
    content: str
    metadata: Dict[str, Union[str, int, bool]]
