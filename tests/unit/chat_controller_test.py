import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import Request
from fastapi.responses import JSONResponse

from use_cases.chatUseCase import ChatUseCase
from controllers.chatController import ChatController
from models.question import Question


@pytest.fixture
def mock_chat_use_case():
    return MagicMock(spec=ChatUseCase)

@pytest.fixture
def chat_controller(mock_chat_use_case):
    return ChatController(chat_use_case=mock_chat_use_case)

@pytest.fixture
def mock_request():
    return AsyncMock(Request)


# Verifica che il metodo get_answer di ChatController, in caso di messaggio vuoto, restituisca un messaggio di errore

@pytest.mark.asyncio
async def test_process_chat_empty_message(chat_controller, mock_request):
    # Arrange
    mock_request.json.return_value = {"message": ""}

    # Act
    response = await chat_controller.get_answer(mock_request)

    # Assert
    assert isinstance(response, JSONResponse)
    assert response.status_code == 400
    assert response.body == b'{"error":"Messaggio vuoto"}'


# Verifica che il metodo get_answer di ChatController gestisca correttamente le eccezioni

@pytest.mark.asyncio
async def test_process_chat_raises_Exception(chat_controller, mock_chat_use_case, mock_request):
    # Arrange
    mock_request.json.return_value = {"message": "Hello"}

    # Configura il mock per lanciare un'eccezione
    mock_chat_use_case.get_answer.side_effect = Exception("Errore nel recupero della risposta")

    # Act
    with pytest.raises(Exception) as exc_info:
        await chat_controller.get_answer(mock_request)

    # Assert
    assert str(exc_info.value) == "Errore nel recupero della risposta"


# Verifica che il costruttore di ChatController gestisca correttamente le eccezioni

#def test_chat_controller_constructor_raises_Exception():
    # Act
#    with pytest.raises(ValueError) as exc_info:
#        ChatController(chat_use_case=None)

    # Assert
#    assert str(exc_info.value) == "chat_use_case cannot be None"
