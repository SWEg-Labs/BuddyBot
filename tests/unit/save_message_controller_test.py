import pytest
from unittest.mock import MagicMock
from datetime import datetime

from dto.messageDTO import MessageDTO
from models.dbSaveOperationResponse import DbSaveOperationResponse
from models.message import Message, MessageSender
from controllers.saveMessageController import SaveMessageController
from services.saveMessageService import SaveMessageService


# Verifica che il metodo save di SaveMessageController gestisca correttamente un messaggio con sender 'CHATBOT'

def test_save_with_chatbot_sender():
    # Arrange
    mock_save_message_use_case = MagicMock(spec=SaveMessageService)
    save_message_controller = SaveMessageController(mock_save_message_use_case)

    content = "test message"
    timestamp = datetime(2021, 10, 10, 10, 10, 10)
    timestamp_str = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    message_dto = MessageDTO(content, timestamp_str, 'CHATBOT')
    message = Message(content, timestamp, MessageSender.CHATBOT)

    mock_save_message_use_case.save.return_value = DbSaveOperationResponse(True, "Message saved successfully")
    expected_response = {"success": True, "message": "Message saved successfully"}

    # Act
    response = save_message_controller.save(message_dto)

    # Assert
    mock_save_message_use_case.save.assert_called_once_with(message)
    assert response == expected_response


# Verifica che il metodo save di SaveMessageController sollevi un'eccezione per un messaggio avente un sender non valido

def test_save_with_invalid_sender():
    # Arrange
    mock_save_message_use_case = MagicMock(spec=SaveMessageService)
    save_message_controller = SaveMessageController(mock_save_message_use_case)

    content = "test message"
    timestamp = datetime(2021, 10, 10, 10, 10, 10)
    timestamp_str = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    message_dto = MessageDTO(content, timestamp_str, 'INVALID_SENDER')

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        save_message_controller.save(message_dto)
    assert str(exc_info.value) == "Invalid sender: INVALID_SENDER"


# Verifica che il metodo save di SaveMessageController sollevi un'eccezione per un messaggio avente timestamp non valido

def test_save_with_invalid_timestamp():
    # Arrange
    mock_save_message_use_case = MagicMock(spec=SaveMessageService)
    save_message_controller = SaveMessageController(mock_save_message_use_case)

    content = "test message"
    invalid_timestamp_str = "invalid-timestamp"
    message_dto = MessageDTO(content, invalid_timestamp_str, 'USER')

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        save_message_controller.save(message_dto)
    assert str(exc_info.value) == f"Invalid timestamp format: {invalid_timestamp_str}"


# Verifica che il metodo save di SaveMessageController gestisca correttamente le eccezioni generali

def test_save_general_exception():
    # Arrange
    mock_save_message_use_case = MagicMock(spec=SaveMessageService)
    save_message_controller = SaveMessageController(mock_save_message_use_case)

    content = "test message"
    timestamp = datetime(2021, 10, 10, 10, 10, 10)
    timestamp_str = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    message_dto = MessageDTO(content, timestamp_str, 'USER')

    mock_save_message_use_case.save.side_effect = Exception("General error")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        save_message_controller.save(message_dto)
    assert str(exc_info.value) == "General error"
