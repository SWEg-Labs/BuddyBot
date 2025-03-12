from abc import ABC, abstractmethod

from models.lastLoadOutcome import LastLoadOutcome

class GetLastLoadOutcomeUseCase(ABC):
    """
    Interface for the use case to get the last load outcome.
    """

    @abstractmethod
    def get_last_load_outcome(self) -> LastLoadOutcome:
        """
        Abstract method to retrieve the last load outcome.
        Returns:
            LastLoadOutcome: The last load outcome.
        """
