from dto.lastLoadOutcomeDTO import LastLoadOutcomeDTO
from use_cases.getLastLoadOutcomeUseCase import GetLastLoadOutcomeUseCase
from utils.logger import logger
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
class GetLastLoadOutcomeController:
    """
    Controller for handling the retrieval of the last load outcome.
    Attributes:
        get_last_load_outcome_use_case (GetLastLoadOutcomeUseCase): Use case for getting the last load outcome.
    """

    def __init__(self, get_last_load_outcome_use_case: GetLastLoadOutcomeUseCase):
        """
        Initializes the GetLastLoadOutcomeController with the provided use case.
        Args:
            get_last_load_outcome_use_case (GetLastLoadOutcomeUseCase): The use case for getting the last load outcome.
        """
        self.get_last_load_outcome_use_case = get_last_load_outcome_use_case

    def get_last_load_outcome(self) -> LastLoadOutcomeDTO:
        """
        Retrieves the last load outcome.
        Returns:
            LastLoadOutcomeDTO: Data transfer object containing the last load outcome.
        Raises:
            Exception: If there is an error while getting the last load outcome.
        """
        try:
            outcome = self.get_last_load_outcome_use_case.get_last_load_outcome()
            return LastLoadOutcomeDTO(outcome.value)
        except Exception as e:
            logger.error(f"Error getting last load outcome in GetLastLoadOutcomeController: {e}")
            raise e
