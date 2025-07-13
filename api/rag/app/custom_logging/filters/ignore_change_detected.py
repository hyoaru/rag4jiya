import logging


class IgnoreChangeDetected(logging.Filter):
    """Drop 'X change detected' debug lines from uvicorn reload."""

    def filter(self, record: logging.LogRecord) -> bool:
        return "change detected: {" not in record.getMessage()
