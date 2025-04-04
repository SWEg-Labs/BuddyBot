from unittest.mock import MagicMock
from datetime import datetime

from dto.messageDTO import MessageDTO
from models.quantity import Quantity
from models.page import Page
from models.message import Message, MessageSender
from controllers.getMessagesController import GetMessagesController
from use_cases.getMessagesUseCase import GetMessagesUseCase


# Verifica che il metodo get_messages di GetMessagesController chiami il metodo get_messages di GetMessagesUseCase

def test_get_messages_calls_use_case_method():
    # Arrange
    mock_get_messages_use_case = MagicMock(spec=GetMessagesUseCase)
    get_messages_controller = GetMessagesController(mock_get_messages_use_case)

    quantity = 5
    page = 1
    request_data = {"quantity": quantity, "page": page}
    quantity_object = Quantity(quantity)
    page_object = Page(page)
    expected_result = [
        MessageDTO(content=f"Message {i}", timestamp=f"2021-10-10T10:10:{i:02d}.000Z", sender='USER')
        for i in range(quantity)
    ]
    use_case_result = [
        Message(content=f"Message {i}", timestamp=datetime(2021, 10, 10, 10, 10, i),
                               sender=MessageSender.USER) for i in range(quantity)
    ]
    mock_get_messages_use_case.get_messages.return_value = use_case_result

    # Act
    result = get_messages_controller.get_messages(request_data)

    # Assert
    mock_get_messages_use_case.get_messages.assert_called_once_with(quantity_object, page_object)
    assert result == expected_result
