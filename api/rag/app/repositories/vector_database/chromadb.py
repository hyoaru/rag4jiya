import os
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv
from .interface import VectorDatabaseRepositoryABC


class ChromaDbVectorDatabaseRepository(VectorDatabaseRepositoryABC):
    async def async_init(self):
        load_dotenv(override=True)
        self._client = await chromadb.AsyncHttpClient(
            host=os.environ["CHROMADB_HOST"],
            port=int(os.environ["CHROMADB_PORT"]),
        )

        self._embedding_function = OpenAIEmbeddingFunction(
            api_key=os.environ["OPENAI_API_KEY"],
            model_name=os.environ["CHROMADB_OPENAI_EMBEDDING_MODEL"],
        )

    async def get_collection(self, name: str):
        return await self._client.get_collection(name=name)

    async def create_collection(self, name: str):
        collection = await self._client.get_or_create_collection(
            name=name,
            embedding_function=self._embedding_function,  # type: ignore[arg-type]
        )

        return collection

    async def add_vector(
        self,
        collection: str,
        contents: str,
        ids: str,
        metadatas: str,
    ):
        pass
