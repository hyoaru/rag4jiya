from typing import List
from pydantic import BaseModel


class DocumentChunkedToList(BaseModel):
    headings: List[str]
    texts: List[str]
    page_numbers: List[int]
