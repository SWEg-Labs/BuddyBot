from unittest.mock import MagicMock
from datetime import datetime

from models.loggingModels import LoadingAttempt, LoadingItems, PlatformLog, VectorStoreLog
from models.dbSaveOperationResponse import DbSaveOperationResponse
from models.message import Message, MessageSender
from models.quantity import Quantity
from entities.loggingEntities import PostgresLoadingAttempt, PostgresLoadingItems, PostgresPlatformLog, PostgresVectorStoreLog
from entities.postgresSaveOperationResponse import PostgresSaveOperationResponse
from entities.postgresMessage import PostgresMessage, PostgresMessageSender
from adapters.postgresAdapter import PostgresAdapter
from repositories.postgresRepository import PostgresRepository


# Verifica che il metodo save_message di PostgresAdapter chiami il metodo save_message di PostgresRepository

def test_save_message_calls_repository_method():
    # Arrange
    mock_postgres_repository = MagicMock(spec=PostgresRepository)
    postgres_adapter = PostgresAdapter(mock_postgres_repository)

    content = "test message"
    timestamp = "2021-10-10T10:10:10"
    message = Message(content, timestamp, MessageSender.USER)
    postgres_message = PostgresMessage(content, timestamp, PostgresMessageSender.USER)

    mock_postgres_repository.save_message.return_value = PostgresSaveOperationResponse(True, "Message saved successfully")
    expected_response = DbSaveOperationResponse(True, "Message saved successfully")

    # Act
    result = postgres_adapter.save_message(message)

    # Assert
    mock_postgres_repository.save_message.assert_called_once_with(postgres_message)
    assert result == expected_response


# Verifica che il metodo get_messages di PostgresAdapter chiami il metodo get_messages di PostgresRepository

def test_get_messages_calls_repository_method():
    # Arrange
    mock_postgres_repository = MagicMock(spec=PostgresRepository)
    postgres_adapter = PostgresAdapter(mock_postgres_repository)

    quantity = 5
    expected_response = [
        Message(content=f"Message {i}", timestamp=f"2021-10-10T10:10:0{i}",
                sender=MessageSender.USER if i%2==0 else MessageSender.CHATBOT) for i in range(quantity)
    ]

    postgres_messages = [
        PostgresMessage(content=f"Message {i}", timestamp=f"2021-10-10T10:10:0{i}",
                        sender=PostgresMessageSender.USER if i%2==0 else PostgresMessageSender.CHATBOT) for i in range(quantity)
    ]
    mock_postgres_repository.get_messages.return_value = postgres_messages

    # Act
    result = postgres_adapter.get_messages(Quantity(quantity))

    # Assert
    mock_postgres_repository.get_messages.assert_called_once_with(quantity)
    assert result == expected_response


# Verifica che il metodo save_loading_attempt di PostgresAdapter chiami il metodo save_loading_attempt di PostgresRepository

def test_save_loading_attempt_calls_repository_method():
    # Arrange
    mock_postgres_repository = MagicMock(spec=PostgresRepository)
    postgres_adapter = PostgresAdapter(mock_postgres_repository)

    platform_log = PlatformLog(
        loading_items=LoadingItems.GitHubCommits,
        timestamp=datetime(2023, 10, 1, 12, 0, 0),
        outcome=True
    )
    vector_store_log = VectorStoreLog(
        timestamp=datetime(2023, 10, 1, 12, 30, 0),
        outcome=True,
        num_added_items=10,
        num_modified_items=5,
        num_deleted_items=2
    )
    loading_attempt = LoadingAttempt(
        platform_logs=[platform_log],
        vector_store_log=vector_store_log
    )

    postgres_platform_log = PostgresPlatformLog(
        postgres_loading_items=PostgresLoadingItems.GitHubCommits,
        timestamp=datetime(2023, 10, 1, 12, 0, 0),
        outcome=True
    )
    postgres_vector_store_log = PostgresVectorStoreLog(
        timestamp=datetime(2023, 10, 1, 12, 30, 0),
        outcome=True,
        num_added_items=10,
        num_modified_items=5,
        num_deleted_items=2
    )
    postgres_loading_attempt = PostgresLoadingAttempt(
        postgres_platform_logs=[postgres_platform_log],
        postgres_vector_store_log=postgres_vector_store_log
    )

    expected_response = DbSaveOperationResponse(success=True, message="Loading attempt saved successfully")

    postgres_response = PostgresSaveOperationResponse(success=True, message="Loading attempt saved successfully")
    mock_postgres_repository.save_loading_attempt.return_value = postgres_response

    # Act
    result = postgres_adapter.save_loading_attempt(loading_attempt)

    # Assert
    mock_postgres_repository.save_loading_attempt.assert_called_once_with(postgres_loading_attempt)
    assert result == expected_response
