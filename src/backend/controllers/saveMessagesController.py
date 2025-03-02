from use_cases.saveMessageUseCase import SaveMessageUseCase
from models.dbSaveOperationResponse import DbSaveOperationResponse
from dto.messageBaseModel import MessageBaseModel

class SaveMessagesController:
    """
    Controller class for saving messages.
    This class uses the SaveMessageUseCase to save messages and provides a method to handle the save operation.
    Attributes:
        SaveMessageUseCase (SaveMessageUseCase): The use case instance responsible for saving messages.
    Methods:
        save(message: MessageBaseModel) -> dict[str, bool | str]:
    """
    def __init__(self, SaveMessageUseCase: SaveMessageUseCase):
        self.SaveMessageUseCase = SaveMessageUseCase
    
    def save(self, message: MessageBaseModel) -> dict[str, bool | str]:
        """
        Saves a message using the SaveMessageUseCase and returns the result.
        Args:
            message (MessageBaseModel): The message to be saved.
        Returns:
            dict: A dictionary containing the success status and message of the save operation.
        """

        dbSaveOperationResponse = self.SaveMessageUseCase.save(message).__copy__()

        result = {"success": dbSaveOperationResponse.success, "message": dbSaveOperationResponse.message}
        return result