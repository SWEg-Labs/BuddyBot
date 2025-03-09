from enum import Enum

class LastLoadOutcomeDTO(str, Enum):
    TRUE = "True"
    FALSE = "False"
    ERROR = "Error"
