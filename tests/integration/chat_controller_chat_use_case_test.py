import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request
from fastapi.responses import JSONResponse
from services.chatService import ChatService
from use_cases.chatUseCase import ChatUseCase
from controllers.chatController import ChatController

pytestmark = pytest.mark.asyncio  # ✅ Imposta asyncio per tutti i test nel file


# Verifica che il metodo get_answer di ChatController chiami correttamente il metodo get_answer di ChatUseCase, in caso di messaggio non vuoto

async def test_process_chat_calls_process_user_input():
    # Arrange
    mock_chat_use_case = MagicMock(spec=ChatUseCase)
    chat_controller = ChatController(chat_use_case=mock_chat_use_case)
    mock_request = AsyncMock(Request)
    mock_request.json.return_value = {"message": "Hello"}

    # Act
    response = await chat_controller.get_answer(mock_request)

    # Assert
    mock_chat_use_case.process_user_input.assert_called_with("Hello")
    assert response == {"response": mock_chat_use_case.process_user_input.return_value}


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
