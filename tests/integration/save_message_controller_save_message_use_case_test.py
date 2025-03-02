from unittest.mock import MagicMock
from controllers.saveMessageController import SaveMessageController
from use_cases.saveMessageService import SaveMessageService
from dto.messageBaseModel import MessageBaseModel, MessageSenderBaseModel
from models.dbSaveOperationResponse import DbSaveOperationResponse
from models.message import Message, MessageSender


# Verifica che il metodo save di SaveMessageController chiami il metodo save di SaveMessageUseCase

def test_save_calls_use_case_method():
    # Arrange
    mock_save_message_use_case = MagicMock(spec=SaveMessageService)
    save_message_controller = SaveMessageController(mock_save_message_use_case)

    content = "test message"
    timestamp = "2021-10-10T10:10:10"
    message = MessageBaseModel(content, timestamp, MessageSenderBaseModel.User)

    mock_save_message_use_case.save.return_value = DbSaveOperationResponse(True, "Message saved successfully")
    expected_response = {"success": True, "message": "Message saved successfully"}
    
    # Act
    response = save_message_controller.save(message)

    # Assert
    mock_save_message_use_case.save.assert_called_once_with(Message(content,timestamp,MessageSender.USER))
    assert response == expected_response