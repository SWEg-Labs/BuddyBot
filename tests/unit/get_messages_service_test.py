import pytest
from unittest.mock import MagicMock

from models.quantity import Quantity
from models.page import Page
from services.getMessagesService import GetMessagesService
from ports.getMessagesPort import GetMessagesPort


# Verifica che il metodo get_messages di GetMessagesService gestisca correttamente le eccezioni

def test_get_messages_exception():
    # Arrange
    mock_get_messages_port = MagicMock(spec=GetMessagesPort)
    get_messages_service = GetMessagesService(mock_get_messages_port)

    quantity = Quantity(50)
    page = Page(1)
    mock_get_messages_port.get_messages.side_effect = Exception("Port error")

    # Act
    with pytest.raises(Exception) as exc_info:
        get_messages_service.get_messages(quantity, page)

    # Assert
    assert str(exc_info.value) == "Port error"
