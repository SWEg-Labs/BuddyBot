from enum import Enum

class PostgresLastLoadOutcome(Enum):
    TRUE = "True"
    FALSE = "False"
    ERROR = "Error"
