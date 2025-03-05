import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request
from fastapi.responses import JSONResponse
from use_cases.chatUseCase import ChatUseCase
from controllers.chatController import ChatController
from models.question import Question

pytestmark = pytest.mark.asyncio  # ✅ Imposta asyncio per tutti i test nel file


# Verifica che il metodo get_answer di ChatController chiami correttamente il metodo get_answer di ChatUseCase, in caso di messaggio non vuoto

async def test_process_chat_calls_get_answer():
    # Arrange
    mock_chat_use_case = MagicMock(spec=ChatUseCase)
    chat_controller = ChatController(chat_use_case=mock_chat_use_case)
    mock_request = AsyncMock(Request)
    mock_request.json.return_value = {"message": "Hello"}

    # Act
    response = await chat_controller.get_answer(mock_request)

    # Assert
    mock_chat_use_case.get_answer.assert_called_with(Question("Hello"))
    assert response == {"response": mock_chat_use_case.get_answer.return_value.content}


# Verifica che il metodo get_answer di ChatController chiami correttamente il metodo get_answer di ChatUseCase, in caso di messaggio vuoto

async def test_process_chat_empty_message():
    # Arrange
    mock_chat_use_case = MagicMock(spec=ChatUseCase)
    chat_controller = ChatController(chat_use_case=mock_chat_use_case)
    mock_request = AsyncMock(Request)
    mock_request.json.return_value = {"message": ""}

    # Act
    response = await chat_controller.get_answer(mock_request)

    # Assert
    assert isinstance(response, JSONResponse)
    assert response.status_code == 400
    assert response.body == b'{"error":"Messaggio vuoto"}'
