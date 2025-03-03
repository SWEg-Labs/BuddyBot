from unittest.mock import MagicMock

from dto.messageBaseModel import MessageBaseModel, MessageSenderBaseModel
from models.dbSaveOperationResponse import DbSaveOperationResponse
from models.message import Message, MessageSender
from controllers.saveMessageController import SaveMessageController
from services.saveMessageService import SaveMessageService


# Verifica che il metodo save di SaveMessageController chiami il metodo save di SaveMessageUseCase

def test_save_calls_use_case_method():
    # Arrange
    mock_save_message_use_case = MagicMock(spec=SaveMessageService)
    save_message_controller = SaveMessageController(mock_save_message_use_case)

    content = "test message"
    timestamp = "2021-10-10T10:10:10"
    message_base_model = MessageBaseModel(content, timestamp, MessageSenderBaseModel.USER)
    message = Message(content, timestamp, MessageSender.USER)

    mock_save_message_use_case.save.return_value = DbSaveOperationResponse(True, "Message saved successfully")
    expected_response = {"success": True, "message": "Message saved successfully"}

    # Act
    response = save_message_controller.save(message_base_model)

    # Assert
    mock_save_message_use_case.save.assert_called_once_with(message)
    assert response == expected_response
