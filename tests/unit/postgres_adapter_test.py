import pytest
from unittest.mock import MagicMock
from datetime import datetime

from models.loggingModels import LoadingAttempt, LoadingItems, PlatformLog, VectorStoreLog
from models.message import Message, MessageSender
from models.quantity import Quantity
from models.page import Page
from entities.postgresSaveOperationResponse import PostgresSaveOperationResponse
from entities.postgresMessage import PostgresMessage, PostgresMessageSender
from adapters.postgresAdapter import PostgresAdapter
from repositories.postgresRepository import PostgresRepository


# Verifica che il metodo get_messages di PostgresAdapter ritorni una lista vuota se non ci sono messaggi

def test_get_messages_returns_empty_list():
    # Arrange
    mock_postgres_repository = MagicMock(spec=PostgresRepository)
    postgres_adapter = PostgresAdapter(mock_postgres_repository)

    quantity = 5
    page = 1
    mock_postgres_repository.get_messages.return_value = []

    # Act
    result = postgres_adapter.get_messages(Quantity(quantity), Page(page))

    # Assert
    mock_postgres_repository.get_messages.assert_called_once_with(quantity, page)
    assert result == []


# Verifica che il metodo save_message di PostgresAdapter gestisca correttamente le eccezioni

def test_save_message_exception():
    # Arrange
    mock_postgres_repository = MagicMock(spec=PostgresRepository)
    postgres_adapter = PostgresAdapter(mock_postgres_repository)

    content = "test message"
    timestamp = datetime(2021, 10, 10, 10, 10, 10)
    message = Message(content, timestamp, MessageSender.USER)

    mock_postgres_repository.save_message.side_effect = Exception("Save message error")

    # Act
    with pytest.raises(Exception) as exc_info:
        postgres_adapter.save_message(message)

    # Assert
    assert str(exc_info.value) == "Save message error"


# Verifica che il metodo get_messages di PostgresAdapter gestisca correttamente le eccezioni

def test_get_messages_exception():
    # Arrange
    mock_postgres_repository = MagicMock(spec=PostgresRepository)
    postgres_adapter = PostgresAdapter(mock_postgres_repository)

    quantity = 5
    page = 1
    mock_postgres_repository.get_messages.side_effect = Exception("Get messages error")

    # Act
    with pytest.raises(Exception) as exc_info:
        postgres_adapter.get_messages(Quantity(quantity), Page(page))

    # Assert
    assert str(exc_info.value) == "Get messages error"


# Verifica che il metodo save_loading_attempt di PostgresAdapter gestisca correttamente le eccezioni

def test_save_loading_attempt_exception():
    # Arrange
    mock_postgres_repository = MagicMock(spec=PostgresRepository)
    postgres_adapter = PostgresAdapter(mock_postgres_repository)

    platform_log = PlatformLog(
        loading_items=LoadingItems.GitHubCommits,
        timestamp=datetime(2023, 10, 1, 12, 0, 0),
        outcome=True
    )
    vector_store_log = VectorStoreLog(
        timestamp=datetime(2023, 10, 1, 12, 5, 0),
        outcome=True,
        num_added_items=10,
        num_modified_items=5,
        num_deleted_items=2
    )
    loading_attempt = LoadingAttempt(
        platform_logs=[platform_log],
        vector_store_log=vector_store_log,
        starting_timestamp=datetime(2023, 10, 1, 11, 55, 0)
    )

    mock_postgres_repository.save_loading_attempt.side_effect = Exception("Save loading attempt error")

    # Act
    with pytest.raises(Exception) as exc_info:
        postgres_adapter.save_loading_attempt(loading_attempt)

    # Assert
    assert str(exc_info.value) == "Save loading attempt error"


# Verifica che il metodo get_last_load_outcome di PostgresAdapter gestisca correttamente le eccezioni

def test_get_last_load_outcome_exception():
    # Arrange
    mock_postgres_repository = MagicMock(spec=PostgresRepository)
    postgres_adapter = PostgresAdapter(mock_postgres_repository)

    mock_postgres_repository.get_last_load_outcome.side_effect = Exception("Get last load outcome error")

    # Act
    with pytest.raises(Exception) as exc_info:
        postgres_adapter.get_last_load_outcome()

    # Assert
    assert str(exc_info.value) == "Get last load outcome error"


# Verifica che il metodo __dsor_converter di PostgresAdapter sollevi un'eccezione ValueError se il messaggio è vuoto

def test_dsor_converter_value_error_empty_message():
    # Arrange
    mock_postgres_repository = MagicMock(spec=PostgresRepository)
    postgres_adapter = PostgresAdapter(mock_postgres_repository)
    psor = PostgresSaveOperationResponse(success=True, message="")

    # Act
    with pytest.raises(ValueError) as exc_info:
        postgres_adapter._PostgresAdapter__dsor_converter(psor)

    # Assert
    assert str(exc_info.value) == "The message is empty."


# Verifica che il metodo __postgres_message_converter di PostgresAdapter sollevi un'eccezione ValueError se il contenuto è vuoto

def test_postgres_message_converter_value_error_empty_content():
    # Arrange
    mock_postgres_repository = MagicMock(spec=PostgresRepository)
    postgres_adapter = PostgresAdapter(mock_postgres_repository)
    message = Message(content="", timestamp=datetime.now(), sender=MessageSender.USER)

    # Act
    with pytest.raises(ValueError) as exc_info:
        postgres_adapter._PostgresAdapter__postgres_message_converter(message)

    # Assert
    assert str(exc_info.value) == "The content is empty."


# Verifica che il metodo __message_converter di PostgresAdapter sollevi un'eccezione ValueError se il contenuto è vuoto

def test_message_converter_value_error_empty_content():
    # Arrange
    mock_postgres_repository = MagicMock(spec=PostgresRepository)
    postgres_adapter = PostgresAdapter(mock_postgres_repository)
    postgres_message = PostgresMessage(content="", timestamp=datetime.now(), sender=PostgresMessageSender.USER)

    # Act
    with pytest.raises(ValueError) as exc_info:
        postgres_adapter._PostgresAdapter__message_converter(postgres_message)

    # Assert
    assert str(exc_info.value) == "The content is empty."


# Verifica che il metodo __postgres_loading_attempt_converter di PostgresAdapter sollevi un'eccezione ValueError se i platform logs sono vuoti

def test_postgres_loading_attempt_converter_value_error_empty_platform_logs():
    # Arrange
    mock_postgres_repository = MagicMock(spec=PostgresRepository)
    postgres_adapter = PostgresAdapter(mock_postgres_repository)
    loading_attempt = LoadingAttempt(
        platform_logs=[],
        vector_store_log=VectorStoreLog(
            timestamp=datetime.now(),
            outcome=True,
            num_added_items=10,
            num_modified_items=5,
            num_deleted_items=2
        ),
        starting_timestamp=datetime.now()
    )

    # Act
    with pytest.raises(ValueError) as exc_info:
        postgres_adapter._PostgresAdapter__postgres_loading_attempt_converter(loading_attempt)

    # Assert
    assert str(exc_info.value) == "The platform logs are empty."
