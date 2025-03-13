import pytest
from unittest.mock import MagicMock
from datetime import datetime

from models.message import Message, MessageSender
from services.saveMessageService import SaveMessageService
from ports.saveMessagePort import SaveMessagePort


# Verifica che il metodo save di SaveMessageService gestisca correttamente le eccezioni

def test_save_handles_exception():
    # Arrange
    mock_save_message_port = MagicMock(spec=SaveMessagePort)
    save_message_service = SaveMessageService(mock_save_message_port)

    content = "test message"
    timestamp = datetime(2021, 10, 10, 10, 10, 10)
    message = Message(content, timestamp, MessageSender.USER)

    mock_save_message_port.save_message.side_effect = Exception("Save message error")

    # Act
    with pytest.raises(Exception) as exc_info:
        save_message_service.save(message)

    # Assert
    assert str(exc_info.value) == "Save message error"
