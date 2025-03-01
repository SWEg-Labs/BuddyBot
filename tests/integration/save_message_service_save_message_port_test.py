from unittest.mock import MagicMock
from dto.messageDtos import Message
from services.saveMessageService import SaveMessageService
from ports.saveMessagePort import SaveMessagePort
from models.dbSaveOperationResponse import DbSaveOperationResponse
from dto.messageDtos import MessageSender

# Verifica che il metodo save di SaveMessageService chiami il metodo save_message di SaveMessagePort

def test_save_calls_port_method():
    # Arrange
    mock_save_message_port = MagicMock(spec=SaveMessagePort)
    save_message_service = SaveMessageService(mock_save_message_port)

    content = "test message"
    timestamp = "2021-10-10T10:10:10"
    message = Message(content, timestamp, MessageSender.USER)

    mock_save_message_port.save_message.return_value = DbSaveOperationResponse(success=True, message="Message saved successfully")
    expected_response = DbSaveOperationResponse(success=True, message="Message saved successfully")

    # Act
    result = save_message_service.save(message)

    # Assert
    mock_save_message_port.save_message.assert_called_once_with(message)
    assert result == expected_response