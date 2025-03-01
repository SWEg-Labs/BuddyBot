from unittest.mock import MagicMock

from models.loading_attempt import LoadingAttempt
from models.postgres_loading_attempt import PostgresLoadingAttempt
from models.db_save_operation_response import DbSaveOperationResponse
from entities.postgres_save_operation_response import PostgresSaveOperationResponse
from adapters.postgres_adapter import PostgresAdapter
from repositories.postgres_repository import PostgresRepository
from dto.messageDtos import Message, MesssageSender
from dto.quantity import Quantity
from entities.postgresEntities import PostgresMessage, PostgresMesssageSender


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


# Verifica che il metodo save_message di PostgresAdapter chiami il metodo save_message di PostgresRepository

def test_save_message_calls_repository_method():
    # Arrange
    mock_postgres_repository = MagicMock(spec=PostgresRepository)
    postgres_adapter = PostgresAdapter(mock_postgres_repository)

    content = "test message"
    timestamp = "2021-10-10T10:10:10"
    message = Message(content, timestamp, MesssageSender.USER)

    mock_postgres_repository.save_message.return_value = PostgresSaveOperationResponse(True, "Message saved successfully")
    expected_response = DbSaveOperationResponse(True, "Message saved successfully")

    # Act
    result = postgres_adapter.save_message(message)

    # Assert
    mock_postgres_repository.save_message.assert_called_once_with(message)
    assert result == expected_response


# Verifica che il metodo get_messages di PostgresAdapter chiami il metodo get_messages di PostgresRepository

def test_get_messages_calls_repository_method():
    # Arrange
    mock_postgres_repository = MagicMock(spec=PostgresRepository)
    postgres_adapter = PostgresAdapter(mock_postgres_repository)

    quantity = 5

    expected_response = [
        PostgresMessage(content=f"Message {i}", timestamp=f"2021-10-10T10:10:0{i}", sender=PostgresMesssageSender.USER) for i in range(quantity)
    ]
    mock_postgres_repository.get_messages.return_value = expected_response

    # Act
    result = postgres_adapter.get_messages()

    # Assert
    mock_postgres_repository.get_messages.assert_called_once_with(quantity)
    assert result == expected_response