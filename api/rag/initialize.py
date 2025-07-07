import asyncio
from app.services.document_vector_collection import DocumentVectorCollectionService


async def main():
    print("Running initial migrations...")
    await DocumentVectorCollectionService().apply_migrations()
    print("Migrations completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())
