from abc import ABC, abstractmethod
from typing import Any

from fastapi import UploadFile


class DocumentVectorCollectionServiceABC(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def apply_migrations(self):
        pass

    @abstractmethod
    async def similarity_search_across_documents(self, user_id: str, text: str) -> Any:
        pass

    @abstractmethod
    async def upload_document(
        self,
        user_id: str,
        document: UploadFile,
        document_type: str,
    ):
        pass
