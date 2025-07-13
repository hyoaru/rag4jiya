import atexit
import json
import logging
import logging.config
from logging.handlers import QueueHandler, QueueListener
from pathlib import Path
from typing import cast


class CustomLogger:
    @staticmethod
    def setup_logging():
        config_file = Path(__file__).with_name("logging.conf.json")
        with open(config_file) as f_in:
            config = json.load(f_in)

        logging.config.dictConfig(config)
        queue_handler = cast(QueueHandler, logging.getHandlerByName("queue"))
        if queue_handler is not None:
            queue_listener = cast(QueueListener, queue_handler.listener)
            queue_listener.start()
            atexit.register(queue_listener.stop)

    @staticmethod
    def get_instance():
        return logging.getLogger("app")
