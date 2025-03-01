from unittest.mock import MagicMock
from controllers.saveMessageController import SaveMessageController
from use_cases.saveMessageService import SaveMessageService
from models.messageBaseModel import MessageBaseModel
from dto.dbSaveOperationResponse import DbSaveOperationResponse
from dto.messageDtos import Message
from models.messageBaseModel import MesssageSenderBaseModel
from dto.messageDtos import MessageSender


# Verifica che il metodo save di SaveMessageController chiami il metodo save di SaveMessageUseCase

def test_save_calls_use_case_method():
    # Arrange
    mock_save_message_use_case = MagicMock(spec=SaveMessageService)
    save_message_controller = SaveMessageController(mock_save_message_use_case)

    content = "test message"
    timestamp = "2021-10-10T10:10:10"
    message = MessageBaseModel(content, timestamp, MesssageSenderBaseModel.User)

    mock_save_message_use_case.save.return_value = DbSaveOperationResponse(True, "Message saved successfully")
    expected_response = {"success": True, "message": "Message saved successfully"}
    
    # Act
    response = save_message_controller.save(message)

    # Assert
    mock_save_message_use_case.save.assert_called_once_with(Message(content,timestamp,MessageSender.User))
    assert response == expected_response