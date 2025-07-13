from enum import Enum


class DocumentType(str, Enum):
    TRANSCRIPTION = "transcription"
    HANDBOOK = "handbook"
