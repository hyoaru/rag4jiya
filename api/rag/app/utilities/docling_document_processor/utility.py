import concurrent.futures
import tempfile
from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from docling_core.types.doc.document import DoclingDocument
from fastapi import UploadFile

from app.utilities.docling_document_processor.models.document_chunk import DocumentChunk
from app.utilities.docling_document_processor.models.document_chunked_to_list import (
    DocumentChunkedToList,
)


class DoclingDocumentProcessorUtility:
    @staticmethod
    async def to_docling(document: UploadFile):
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True

        document_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options,
                )
            }
        )

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp:
            tmp.write(await document.read())
            tmp_path = tmp.name

            conversion_result = document_converter.convert(Path(tmp_path))

        return conversion_result.document

    @staticmethod
    def chunk(dl_document: DoclingDocument):
        chunker = HybridChunker()
        chunks = list(chunker.chunk(dl_doc=dl_document))

        def process_chunk(chunk):
            metadata = chunk.meta.export_json_dict()
            document_chunk = DocumentChunk(
                heading=metadata["headings"][0],
                text=chunker.contextualize(chunk=chunk),
                page_number=metadata["doc_items"][0]["prov"][0]["page_no"],
            )

            return document_chunk

        with concurrent.futures.ThreadPoolExecutor() as executor:
            processed_document_chunks = list(executor.map(process_chunk, chunks))

        return processed_document_chunks

    @staticmethod
    def chunk_to_lists(dl_document: DoclingDocument):
        chunker = HybridChunker()
        chunks = list(chunker.chunk(dl_doc=dl_document))

        def process_chunk(chunk):
            metadata = chunk.meta.export_json_dict()
            heading = metadata["headings"][0] if metadata["headings"] else None
            text = chunker.contextualize(chunk=chunk)
            page_number = metadata["doc_items"][0]["prov"][0]["page_no"]
            return heading, text, page_number

        with concurrent.futures.ThreadPoolExecutor() as executor:
            processed = list(executor.map(process_chunk, chunks))

        # Unpack into separate lists
        headings, texts, page_numbers = zip(*processed) if processed else ([], [], [])

        return DocumentChunkedToList(
            headings=list(headings),
            texts=list(texts),
            page_numbers=list(page_numbers),
        )
