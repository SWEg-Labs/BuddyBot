from models.lastLoadOutcome import LastLoadOutcome
from use_cases.getLastLoadOutcomeUseCase import GetLastLoadOutcomeUseCase
from ports.getLastLoadOutcomePort import GetLastLoadOutcomePort
from utils.logger import logger

class GetLastLoadOutcomeService(GetLastLoadOutcomeUseCase):
    """
    Service class to handle the retrieval of the last load outcome.
    Attributes:
        get_last_load_outcome_port (GetLastLoadOutcomePort): Port to access the last load outcome data.
    """

    def __init__(self, get_last_load_outcome_port: GetLastLoadOutcomePort):
        """
        Initializes the GetLastLoadOutcomeService with the provided port.
        Args:
            get_last_load_outcome_port (GetLastLoadOutcomePort): Port to access the last load outcome data.
        Raises:
            Exception: If there is an error during initialization.
        """
        try:
            self.get_last_load_outcome_port = get_last_load_outcome_port
        except Exception as e:
            logger.error(f"Error initializing GetLastLoadOutcomeService: {e}")
            raise e

    def get_last_load_outcome(self) -> LastLoadOutcome:
        """
        Retrieves the last load outcome using the provided port.
        Returns:
            LastLoadOutcome: The last load outcome data.
        Raises:
            Exception: If there is an error during the retrieval process.
        """
        try:
            return self.get_last_load_outcome_port.get_last_load_outcome()
        except Exception as e:
            logger.error(f"Error getting last load outcome in GetLastLoadOutcomeService: {e}")
            raise e
