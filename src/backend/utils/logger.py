import os
import time
import sys
import logging
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

# Imposta il fuso orario italiano, se la funzione tzset esiste (Solo su sistemi Unix/Linux)
os.environ["TZ"] = "Europe/Rome"
if hasattr(time, "tzset"):
    time.tzset()

LOGGING_ENABLED = os.getenv("LOGGING_ENABLED", "true").lower() == "true"
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs_db_update.txt")


### LOGGER 1: Logging standard su stdout ###
logger = logging.getLogger("console_logger")
logger.setLevel(logging.DEBUG if LOGGING_ENABLED else logging.WARNING)

# Crea un handler per scrivere su sys.stdout (console)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s"))

logger.addHandler(console_handler)


### LOGGER 2: Logging standard su file (plain_file_logger) ###

file_logger = logging.getLogger("plain_file_logger")
file_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setFormatter(logging.Formatter("%(message)s"))

file_logger.addHandler(file_handler)
