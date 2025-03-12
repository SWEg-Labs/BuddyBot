from unittest.mock import MagicMock
from datetime import datetime

from models.message import Message, MessageSender
from models.quantity import Quantity
from services.getMessagesService import GetMessagesService
from ports.getMessagesPort import GetMessagesPort


# Verifica che il metodo get_messages di GetMessagesService chiami il metodo get_messages di GetMessagesPort

def test_get_messages_calls_port_method():
    # Arrange
    mock_get_messages_port = MagicMock(spec=GetMessagesPort)
    get_messages_service = GetMessagesService(mock_get_messages_port)

    quantity = 5
    quantity_object = Quantity(quantity)
    expected_result = [Message(content=f"Message {i}", timestamp=datetime(2021, 10, 10, 10, 10, i),
                               sender=MessageSender.USER) for i in range(quantity)]
    mock_get_messages_port.get_messages.return_value = expected_result

    # Act
    result = get_messages_service.get_messages(quantity_object)

    # Assert
    mock_get_messages_port.get_messages.assert_called_once_with(quantity_object)
    assert result == expected_result
