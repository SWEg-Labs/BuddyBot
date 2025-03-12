from unittest.mock import MagicMock
from datetime import datetime

from dto.messageDTO import MessageDTO
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
    timestamp = datetime(2021, 10, 10, 10, 10, 10)
    timestamp_str = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    message_dto = MessageDTO(content, timestamp_str, 'USER')
    message = Message(content, timestamp, MessageSender.USER)

    mock_save_message_use_case.save.return_value = DbSaveOperationResponse(True, "Message saved successfully")
    expected_response = {"success": True, "message": "Message saved successfully"}

    # Act
    response = save_message_controller.save(message_dto)

    # Assert
    mock_save_message_use_case.save.assert_called_once_with(message)
    assert response == expected_response
