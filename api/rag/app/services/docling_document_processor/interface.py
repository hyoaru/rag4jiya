from abc import ABC, abstractmethod
from typing import List

from docling_core.types.doc.document import DoclingDocument
from fastapi import UploadFile

from app.common.models.document_chunk import DocumentChunk


class DoclingDocumentProcessorABC(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def to_docling_document(self, document: UploadFile) -> DoclingDocument:
        pass

    @abstractmethod
    def chunk(self, dl_document: DoclingDocument) -> List[DocumentChunk]:
        pass
