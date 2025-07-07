from typing import List
from pydantic import BaseModel


class DocumentChunkEmbedded(BaseModel):
    heading: str
    text: str
    text_embeddings: List[float]
    page_number: int
