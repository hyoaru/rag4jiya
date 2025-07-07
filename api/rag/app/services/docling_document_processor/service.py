import tempfile
import concurrent.futures
from pathlib import Path

from fastapi import UploadFile
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from docling_core.types.doc.document import DoclingDocument

from app.common.models.document_chunk import DocumentChunk

from .interface import DoclingDocumentProcessorABC


class DoclingDocumentProcessor(DoclingDocumentProcessorABC):
    def __init__(self):
        pass

    async def to_docling_document(self, document: UploadFile):
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

    def chunk(self, dl_document: DoclingDocument):
        chunker = HybridChunker()
        chunks = list(chunker.chunk(dl_doc=dl_document))

        def process_chunk(chunk):
            metadata = chunk.meta.export_json_dict()
            document_chunk = DocumentChunk(
                heading=metadata["headings"][0],
                enriched_text=chunker.contextualize(chunk=chunk),
                page_number=metadata["doc_items"][0]["prov"][0]["page_no"],
            )

            return document_chunk

        with concurrent.futures.ThreadPoolExecutor() as executor:
            processed_document_chunks = list(executor.map(process_chunk, chunks))

        return processed_document_chunks
