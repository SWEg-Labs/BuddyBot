import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request
from fastapi.responses import JSONResponse

from use_cases.chatUseCase import ChatUseCase
from controllers.chatController import ChatController
from models.question import Question


# Verifica che il metodo get_answer di ChatController, in caso di messaggio non vuoto, restituisca la risposta corretta

@pytest.mark.asyncio
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
    assert response == {"response": mock_chat_use_case.get_answer.return_value.get_content()}


# Verifica che il metodo get_answer di ChatController, in caso di messaggio vuoto, restituisca un messaggio di errore

@pytest.mark.asyncio
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


# Verifica che il metodo get_answer di ChatController gestisca correttamente le eccezioni

@pytest.mark.asyncio
async def test_process_chat_raises_exception():
    # Arrange
    mock_chat_use_case = MagicMock(spec=ChatUseCase)
    chat_controller = ChatController(chat_use_case=mock_chat_use_case)
    mock_request = AsyncMock(Request)
    mock_request.json.return_value = {"message": "Hello"}

    # Configura il mock per lanciare un'eccezione
    mock_chat_use_case.get_answer.side_effect = Exception("Errore nel recupero della risposta")

    # Act
    with pytest.raises(Exception) as exc_info:
        await chat_controller.get_answer(mock_request)

    # Assert
    assert str(exc_info.value) == "Errore nel recupero della risposta"


# Verifica che il costruttore di ChatController gestisca correttamente le eccezioni

def test_chat_controller_constructor_raises_exception():
    # Act
    with pytest.raises(ValueError) as exc_info:
        ChatController(chat_use_case=None)

    # Assert
    assert str(exc_info.value) == "chat_use_case cannot be None"
