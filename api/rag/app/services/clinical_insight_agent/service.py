from pydantic_ai import Agent, RunContext, format_as_xml

from app.common.models import DocumentType
from app.services.clinical_insight_agent.agent_models.factory import AgentModelFactory
from app.services.clinical_insight_agent.models.agent_dependencies import (
    AgentDependencies,
)
from app.services.document_vector_collection.service import (
    DocumentVectorCollectionService,
)


class ClinicalInsightAgentService:
    def __init__(self):
        self._agent = Agent(
            model=AgentModelFactory.create("openai"),
            deps_type=AgentDependencies,
            output_type=str,
            system_prompt="""
                # Role
                You are a Clinical Insigt AI Agent assistant designed to retrieve and summarize information from a comprehensive database of nursing documents.
                Your goal is to provide accurate, relevant, and concise responses to user queries while citing the original documents and their page numbers.

                # Task
                1. Analyze the user's input to identify key topics, specific questions, or requests for information.
                2. Determine whether the user would like to retrieve information from transcription, handbook, or both. Use both by default of not indicated.
                3. Summarize the main points from the retrieved documents, ensuring that you capture essential details related to the user’s request.
                4. For every piece of information provided, include citations that reference the original document along with specific page numbers.
                5. Present the information in a clear and organized manner, making it easy for the user to understand and utilize.

                When a task requires using one or more of the tools, make sure to identify which tool is the most appropriate,
                pass along relevant details and execute the actions needed to complete the task.
                Your goal is to be proactive, precise, and organized in managing these resources.
            """,
        )

        @self._agent.system_prompt
        async def add_context(ctx: RunContext[AgentDependencies]):
            return f"The user is asking information about: {ctx.deps.query}"

        @self._agent.tool
        async def search_transcriptions(ctx: RunContext[AgentDependencies]):
            documents = await ctx.deps.document_vector_collection_service.similarity_search_across_documents(
                user_id=ctx.deps.user_id,
                document_type=DocumentType.TRANSCRIPTION,
                text=ctx.deps.query,
            )

            return f"You have the following transcription documents at your disposal:\n {format_as_xml(documents)}"

        @self._agent.tool
        async def search_handbooks(ctx: RunContext[AgentDependencies]):
            documents = await ctx.deps.document_vector_collection_service.similarity_search_across_documents(
                user_id=ctx.deps.user_id,
                document_type=DocumentType.HANDBOOK,
                text=ctx.deps.query,
            )

            return f"You have the following handbook documents at your disposal:\n {format_as_xml(documents)}"

    async def run(self, query: str, user_id: str):
        run_result = await self._agent.run(
            deps=AgentDependencies(
                query=query,
                user_id=user_id,
                document_vector_collection_service=DocumentVectorCollectionService(),
            )
        )

        return run_result.output
