from pydantic import BaseModel


class DocumentChunk(BaseModel):
    heading: str
    enriched_text: str
    page_number: int
