from abc import ABC, abstractmethod

from models.lastLoadOutcome import LastLoadOutcome

class GetLastLoadOutcomePort(ABC):
    """
    Interface for retrieving the last load outcome from a database.
    """

    @abstractmethod
    def get_last_load_outcome(self) -> LastLoadOutcome:
        """
        Abstract method to retrieve the last load outcome from a database.
        Returns:
            LastLoadOutcome: The last load outcome.
        """
        pass
