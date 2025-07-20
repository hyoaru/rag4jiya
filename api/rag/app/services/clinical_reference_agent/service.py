from typing import Dict, List

from pydantic_ai import Agent, RunContext, format_as_xml

from app.common.models import DocumentType
from app.common.models.document_chunk_metadata import DocumentChunkMetadata

from .agent_models.factory import AgentModelFactory
from .models.agent_dependencies import AgentDependencies


class ClinicalReferenceAgentService:
    def __init__(self):
        self._agent = Agent(
            model=AgentModelFactory.create("openai"),
            deps_type=AgentDependencies,
            output_type=str,
            system_prompt="""
                # Role
                You are a Clinical Reference AI assistant.
                Your job is to read the document chunks the system hands you and craft accurate, concise answers—always citing the supplied sources with their page numbers.

                # Inputs You Receive
                A list of pre-selected document chunks inside `<references>` that contains:
                - user_id
                - document_id
                - document_type   (handbook|transcription)
                - document_title
                - heading
                - page_number
                - content   (text)

                You never fetch information yourself; use only what is inside `<references>`.

                # Task
                1. Analyse the user query and the provided references.
                2. Extract the facts that directly answer the query.
                3. Synthesize a clear response in professional nursing language.
                4. After every factual statement, cite the source in this form: `(document_title:page_number)`.
                    - If you combine multiple chunks, cite each relevant page once.
                5. If the references don’t contain enough info, reply: “No information found in provided references.”

                # Style
                - Prefer bullet‑points for lists.
                - Be concise—~2 paragraphs or fewer unless detail is requested.
                - Do not invent data or citations.
                - Keep markdown formatting minimal (headings, bullets are OK).
            """,
        )

        @self._agent.system_prompt
        async def add_context(ctx: RunContext[AgentDependencies]):
            query = format_as_xml(ctx.deps.query, root_tag="user_query")
            references = format_as_xml(ctx.deps.references, root_tag="references")
            return f"{query}\n{references}"

    async def run(
        self,
        query: str,
        user_id: str,
        references: Dict[DocumentType, List[DocumentChunkMetadata]],
    ):
        run_result = await self._agent.run(
            deps=AgentDependencies(
                query=query,
                user_id=user_id,
                references=references,
            )
        )

        return run_result.output
