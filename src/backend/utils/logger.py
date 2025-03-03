import os
import structlog
import logging
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

LOGGING_ENABLED = os.getenv("LOGGING_ENABLED", "true").lower() == "true"
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs_new.txt")

### LOGGER 1: Logging standard su console (console_logger) ###
logger = logging.getLogger("console_logger")
logger.setLevel(logging.DEBUG if LOGGING_ENABLED else logging.WARNING)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

### LOGGER 2: Structlog su file (structured_logger) ###
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso", utc=False),  # Usa ora locale
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory()
)

file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setFormatter(logging.Formatter("%(message)s"))

file_logger = logging.getLogger("file_logger")
file_logger.setLevel(logging.INFO)
file_logger.addHandler(file_handler)

structured_logger = structlog.wrap_logger(file_logger)
