from unittest.mock import MagicMock

from controllers.getMessagesController import GetMessagesController
from use_cases.getMessagesUseCase import GetMessagesUseCase
from dto.messageBaseModel import MessageBaseModel, MessageSenderBaseModel
from models.quantity import Quantity
from models.message import Message, MessageSender

# Verifica che il metodo get_messages di GetMessagesController chiami il metodo get_messages di GetMessagesUseCase

def test_get_messages_calls_use_case_method():
    # Arrange
    mock_get_messages_use_case = MagicMock(spec=GetMessagesUseCase)
    get_messages_controller = GetMessagesController(mock_get_messages_use_case)
    
    quantity = 5
    expected_result = [MessageBaseModel(content=f"Message {i}", timestamp=f"2021-10-10T10:10:0{i}", sender=MessageSenderBaseModel.USER) for i in range(quantity)]
    use_case_result = [Message(content=f"Message {i}", timestamp=f"2021-10-10T10:10:0{i}", sender=MessageSender.USER) for i in range(quantity)]
    mock_get_messages_use_case.get_messages.return_value = use_case_result

    # Act
    result = get_messages_controller.get_messages(quantity)

    # Assert
    mock_get_messages_use_case.get_messages.assert_called_once_with(Quantity(quantity))
    assert result == expected_result