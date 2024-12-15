import os

# Ottiene la configurazione LOGGING_ENABLED dalle variabili di ambiente
LOGGING_ENABLED = os.getenv("LOGGING_ENABLED", "false").lower() == "true"

class Logger:
    """
    Utility logger that can be enabled/disabled via environment variables.
    Wraps print with additional formatting and checks.

    Requires the `LOGGING_ENABLED` environment variable to be set to `true` to enable logging.
    """
    @staticmethod
    def info(message: str):
        """
        Logs an informational message.

        Args:
            message (str): The message to log.

        Raises:
            Exception: If an error occurs while logging the message.
        """
        try:
            if LOGGING_ENABLED:
                print(f"[INFO] {message}")
        except Exception as e:
            print(f"Error logging message: {e}")

    @staticmethod
    def error(message: str):
        """
        Logs an error message.

        Args:
            message (str): The error message to log.

        Raises:
            Exception: If an error occurs while logging the message.
        """
        try:
            if LOGGING_ENABLED:
                print(f"[ERROR] {message}")
        except Exception as e:
            print(f"Error logging message: {e}")

logger = Logger()
