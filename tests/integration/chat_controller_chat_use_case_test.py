import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request

from models.question import Question
from models.answer import Answer
from use_cases.chatUseCase import ChatUseCase
from controllers.chatController import ChatController

pytestmark = pytest.mark.asyncio  # Imposta asyncio per tutti i test nel file


# Verifica che il metodo get_answer di ChatController chiami il metodo get_answer di ChatUseCase

async def test_process_chat_calls_get_answer():
    # Arrange
    mock_chat_use_case = MagicMock(spec=ChatUseCase)
    chat_controller = ChatController(chat_use_case=mock_chat_use_case)
    mock_request = AsyncMock(Request)
    mock_request.json.return_value = {"message": "Hello"}
    answer = Answer("Hello, how can I help you?")
    mock_chat_use_case.get_answer.return_value = answer
    expected_response = {"response": answer.get_content()}

    # Act
    response = await chat_controller.get_answer(mock_request)

    # Assert
    mock_chat_use_case.get_answer.assert_called_with(Question("Hello"))
    assert response == expected_response
