from pathlib import Path
from decouple import config
from json import load
import atexit
import logging
import logging.config
import logging.handlers

def setup_logging() -> None:
    """
    Setup logging framework and create the log file.
    """
    Path(config("path_log_folder")).mkdir(parents=True, exist_ok=True)
    with open(config("path_log_config")) as f:
        logging.config.dictConfig(load(f))
    queue_handler: logging.handlers.QueueHandler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)
