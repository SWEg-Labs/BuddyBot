import os

# Ottiene la configurazione LOGGING_ENABLED dalle variabili di ambiente
LOGGING_ENABLED = os.getenv("LOGGING_ENABLED", "false").lower() == "true"

# Utility logger che può essere attivato/disattivato tramite variabili di ambiente
# Wrappa print con formattazione e controllo aggiuntivi
class Logger:
    @staticmethod
    def info(message: str):
        try:
            if LOGGING_ENABLED:
                print(f"[INFO] {message}")
        except Exception as e:
            print(f"Error logging message: {e}")

    @staticmethod
    def error(message: str):
        try:
            if LOGGING_ENABLED:
                print(f"[ERROR] {message}")
        except Exception as e:
            print(f"Error logging message: {e}")

logger = Logger()
