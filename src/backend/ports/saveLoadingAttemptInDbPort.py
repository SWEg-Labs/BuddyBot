from abc import ABC, abstractmethod

from models.loggingModels import LoadingAttempt
from models.dbSaveOperationResponse import DbSaveOperationResponse

class SaveLoadingAttemptInDbPort(ABC):
    """
    Interface for saving loading attempts to the database.
    This interface defines a method for saving a loading attempt to the database.
    Implementations of this interface should provide the actual logic for saving
    the loading attempt and returning the response from the save operation.
    Methods:
        save_loading_attempt(loading_attempt: LoadingAttempt) -> DbSaveOperationResponse:
    """
    @abstractmethod
    def save_loading_attempt(self, loading_attempt: LoadingAttempt) -> DbSaveOperationResponse:
        """
        Save a loading attempt to the database.
        
        Args:
            loading_attempt (LoadingAttempt): The loading attempt to be saved.
        
        Returns:
            DbSaveOperationResponse: The response from the save operation.
        """
        pass