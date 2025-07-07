from pydantic import BaseModel


class DocumentChunk(BaseModel):
    heading: str
    text: str
    page_number: int
