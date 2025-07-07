from typing import List
from pydantic import BaseModel


class DocumentChunk(BaseModel):
    heading: str
    enriched_text: str
    enriched_text_embedded: List[float]
    page_number: int
