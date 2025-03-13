import pytest
from unittest.mock import MagicMock

from controllers.getMessagesController import GetMessagesController
from use_cases.getMessagesUseCase import GetMessagesUseCase


# Verifica che il metodo get_messages di GetMessagesController gestisca correttamente le eccezioni

def test_get_messages_exception():
    # Arrange
    mock_get_messages_use_case = MagicMock(spec=GetMessagesUseCase)
    get_messages_controller = GetMessagesController(mock_get_messages_use_case)

    quantity_dict = {"value": 5}
    mock_get_messages_use_case.get_messages.side_effect = Exception("Retrieval error")

    # Act
    with pytest.raises(Exception) as exc_info:
        get_messages_controller.get_messages(quantity_dict)

    # Assert
    assert str(exc_info.value) == "Retrieval error"


# Verifica che il metodo get_messages di GetMessagesController restituisca una lista vuota se il metodo get_messages di
# GetMessagesUseCase restituisce una lista vuota

def test_get_messages_empty_list():
    # Arrange
    mock_get_messages_use_case = MagicMock(spec=GetMessagesUseCase)
    get_messages_controller = GetMessagesController(mock_get_messages_use_case)

    quantity_dict = {"value": 5}
    mock_get_messages_use_case.get_messages.return_value = []

    # Act
    result = get_messages_controller.get_messages(quantity_dict)

    # Assert
    assert result == []
