from unittest.mock import MagicMock

from controllers.getMessagesController import GetMessagesController
from use_cases.getMessagesUseCase import GetMessagesUseCase
from models.messageBaseModel import MessageBaseModel, MessageSenderBaseModel

# Verifica che il metodo get_messages di GetMessagesController chiami il metodo get_messages di GetMessagesUseCase

def test_get_messages_calls_use_case_method():
    # Arrange
    mock_get_messages_use_case = MagicMock(spec=GetMessagesUseCase)
    get_messages_controller = GetMessagesController(mock_get_messages_use_case)
    
    quantity = 5
    expected_result = [MessageBaseModel(content=f"Message {i}", timestamp=f"2021-10-10T10:10:0{i}", sender=MessageSenderBaseModel.User) for i in range(quantity)]
    mock_get_messages_use_case.get_messages.return_value = expected_result

    # Act
    result = get_messages_controller.get_messages(quantity)

    # Assert
    mock_get_messages_use_case.get_messages.assert_called_once_with(quantity)
    assert result == expected_result