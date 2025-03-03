from unittest.mock import MagicMock

from models.message import Message, MessageSender
from models.dbSaveOperationResponse import DbSaveOperationResponse
from services.saveMessageService import SaveMessageService
from ports.saveMessagePort import SaveMessagePort

# Verifica che il metodo save di SaveMessageService chiami il metodo save_message di SaveMessagePort

def test_save_calls_port_method():
    # Arrange
    mock_save_message_port = MagicMock(spec=SaveMessagePort)
    save_message_service = SaveMessageService(mock_save_message_port)

    content = "test message"
    timestamp = "2021-10-10T10:10:10"
    message = Message(content, timestamp, MessageSender.USER)

    expected_response = DbSaveOperationResponse(success=True, message="Message saved successfully")
    mock_save_message_port.save_message.return_value = expected_response

    # Act
    result = save_message_service.save(message)

    # Assert
    mock_save_message_port.save_message.assert_called_once_with(message)
    assert result == expected_response
