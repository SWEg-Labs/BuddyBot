from unittest.mock import MagicMock

from dto.messageDTO import MessageDTO, MessageSenderDTO
from models.quantity import Quantity
from models.message import Message, MessageSender
from controllers.getMessagesController import GetMessagesController
from use_cases.getMessagesUseCase import GetMessagesUseCase


# Verifica che il metodo get_messages di GetMessagesController chiami il metodo get_messages di GetMessagesUseCase

def test_get_messages_calls_use_case_method():
    # Arrange
    mock_get_messages_use_case = MagicMock(spec=GetMessagesUseCase)
    get_messages_controller = GetMessagesController(mock_get_messages_use_case)

    quantity = 5
    quantity_dict = {"value": quantity}
    quantity_object = Quantity(quantity)
    expected_result = [
        MessageDTO(content=f"Message {i}", timestamp=f"2021-10-10T10:10:0{i}",
                                        sender=MessageSenderDTO.USER) for i in range(quantity)
    ]
    use_case_result = [
        Message(content=f"Message {i}", timestamp=f"2021-10-10T10:10:0{i}",
                               sender=MessageSender.USER) for i in range(quantity)
    ]
    mock_get_messages_use_case.get_messages.return_value = use_case_result

    # Act
    result = get_messages_controller.get_messages(quantity_dict)

    # Assert
    mock_get_messages_use_case.get_messages.assert_called_once_with(quantity_object)
    assert result == expected_result
