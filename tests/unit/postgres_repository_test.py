import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from psycopg2 import Error as Psycopg2Error

from entities.loggingEntities import PostgresLoadingAttempt, PostgresLoadingItems, PostgresPlatformLog, PostgresVectorStoreLog
from entities.postgresSaveOperationResponse import PostgresSaveOperationResponse
from entities.postgresMessage import PostgresMessage, PostgresMessageSender
from entities.postgresLastLoadOutcome import PostgresLastLoadOutcome
from repositories.postgresRepository import PostgresRepository


@pytest.fixture
def mock_conn():
    return MagicMock()

@pytest.fixture
def postgres_repository(mock_conn):
    return PostgresRepository(mock_conn)


# Verifica che il metodo save_message di PostgresRepository salvi correttamente un messaggio

def test_save_message_success(postgres_repository):
    # Arrange
    message = PostgresMessage("test message", datetime(2021, 10, 10, 10, 10, 10), PostgresMessageSender.USER)
    expected_response = PostgresSaveOperationResponse(success=True, message="Message saved successfully in the Postgres database.")

    with patch.object(postgres_repository, '_PostgresRepository__execute_query', return_value=None):
        # Act
        response = postgres_repository.save_message(message)

    # Assert
    assert response == expected_response


# Verifica che il metodo save_message di PostgresRepository gestisca correttamente un errore del database

def test_save_message_psycopg2_error(postgres_repository):
    # Arrange
    message = PostgresMessage("test message", datetime(2021, 10, 10, 10, 10, 10), PostgresMessageSender.USER)
    with patch.object(postgres_repository, '_PostgresRepository__execute_query', side_effect=Psycopg2Error("DB error")):
        # Act
        response = postgres_repository.save_message(message)

    # Assert
    assert response.get_success() is False
    assert "A connection error occurred" in response.get_message()


# Verifica che il metodo save_message di PostgresRepository gestisca correttamente un'eccezione generica

def test_save_message_exception(postgres_repository):
    # Arrange
    message = PostgresMessage("test message", datetime(2021, 10, 10, 10, 10, 10), PostgresMessageSender.USER)
    with patch.object(postgres_repository, '_PostgresRepository__execute_query', side_effect=Exception("Unexpected error")):
        # Act
        with pytest.raises(Exception) as exc_info:
            postgres_repository.save_message(message)

        # Assert
        assert str(exc_info.value) == "Unexpected error"


# Verifica che il metodo get_messages di PostgresRepository recuperi correttamente i messaggi dal database

def test_get_messages_success(postgres_repository):
    # Arrange
    quantity = 5
    mock_messages = [
        ("Message 1", datetime(2021, 10, 10, 10, 10, 1), PostgresMessageSender.USER.value),
        ("Message 2", datetime(2021, 10, 10, 10, 10, 2), PostgresMessageSender.CHATBOT.value)
    ]
    expected_messages = [
        PostgresMessage("Message 1", datetime(2021, 10, 10, 10, 10, 1), PostgresMessageSender.USER),
        PostgresMessage("Message 2", datetime(2021, 10, 10, 10, 10, 2), PostgresMessageSender.CHATBOT)
    ]

    with patch.object(postgres_repository, '_PostgresRepository__execute_query', return_value=mock_messages):
        # Act
        messages = postgres_repository.get_messages(quantity)

    # Assert
    assert messages == expected_messages


# Verifica che il metodo get_messages di PostgresRepository gestisca correttamente un'eccezione generica

def test_get_messages_exception(postgres_repository):
    # Arrange
    quantity = 5
    with patch.object(postgres_repository, '_PostgresRepository__execute_query', side_effect=Exception("Unexpected error")):
        # Act
        with pytest.raises(Exception) as exc_info:
            postgres_repository.get_messages(quantity)

        # Assert
        assert str(exc_info.value) == "Unexpected error"


# Verifica che il metodo save_loading_attempt di PostgresRepository salvi correttamente un tentativo di caricamento nel database

def test_save_loading_attempt_success(postgres_repository):
    # Arrange
    platform_log = PostgresPlatformLog(PostgresLoadingItems.GitHubCommits, datetime(2023, 10, 1, 12, 0, 0), True)
    vector_store_log = PostgresVectorStoreLog(datetime(2023, 10, 1, 12, 5, 0), True, 10, 5, 2)
    loading_attempt = PostgresLoadingAttempt([platform_log], vector_store_log, datetime(2023, 10, 1, 11, 55, 0))

    expected_response = PostgresSaveOperationResponse(success=True, message="Loading attempt saved successfully in the Postgres database.")

    with patch.object(postgres_repository, '_PostgresRepository__execute_query', return_value=[1]):
        # Act
        response = postgres_repository.save_loading_attempt(loading_attempt)

    # Assert
    assert response == expected_response


# Verifica che il metodo save_loading_attempt di PostgresRepository gestisca correttamente un errore del database

def test_save_loading_attempt_psycopg2_error(postgres_repository):
    # Arrange
    platform_log = PostgresPlatformLog(PostgresLoadingItems.GitHubCommits, datetime(2023, 10, 1, 12, 0, 0), True)
    vector_store_log = PostgresVectorStoreLog(datetime(2023, 10, 1, 12, 5, 0), True, 10, 5, 2)
    loading_attempt = PostgresLoadingAttempt([platform_log], vector_store_log, datetime(2023, 10, 1, 11, 55, 0))

    with patch.object(postgres_repository, '_PostgresRepository__execute_query', side_effect=Psycopg2Error("DB error")):
        # Act
        response = postgres_repository.save_loading_attempt(loading_attempt)

    # Assert
    assert response.get_success() is False
    assert "A connection error occurred" in response.get_message()


# Verifica che il metodo save_loading_attempt di PostgresRepository gestisca correttamente un'eccezione generica

def test_save_loading_attempt_exception(postgres_repository):
    # Arrange
    platform_log = PostgresPlatformLog(PostgresLoadingItems.GitHubCommits, datetime(2023, 10, 1, 12, 0, 0), True)
    vector_store_log = PostgresVectorStoreLog(datetime(2023, 10, 1, 12, 5, 0), True, 10, 5, 2)
    loading_attempt = PostgresLoadingAttempt([platform_log], vector_store_log, datetime(2023, 10, 1, 11, 55, 0))

    with patch.object(postgres_repository, '_PostgresRepository__execute_query', side_effect=Exception("Unexpected error")):
        # Act
        with pytest.raises(Exception) as exc_info:
            postgres_repository.save_loading_attempt(loading_attempt)

        # Assert
        assert str(exc_info.value) == "Unexpected error"


# Verifica che il metodo get_last_load_outcome di PostgresRepository recuperi correttamente l'ultimo esito di caricamento dal database

def test_get_last_load_outcome_success(postgres_repository):
    # Arrange
    with patch.object(postgres_repository, '_PostgresRepository__execute_query', return_value=[(True,)]):
        # Act
        outcome = postgres_repository.get_last_load_outcome()

    # Assert
    assert outcome == PostgresLastLoadOutcome.TRUE


# Verifica che il metodo get_last_load_outcome di PostgresRepository gestisca correttamente il caso in cui non ci siano tuple
# nella tabella degli esiti di caricamento perchè ancora non è stato effettuato alcun caricamento

def test_get_last_load_outcome_no_result(postgres_repository):
    # Arrange
    with patch.object(postgres_repository, '_PostgresRepository__execute_query', return_value=None):
        # Act
        outcome = postgres_repository.get_last_load_outcome()

    # Assert
    assert outcome == PostgresLastLoadOutcome.ERROR


# Verifica che il metodo get_last_load_outcome di PostgresRepository gestisca correttamente un errore del database

def test_get_last_load_outcome_psycopg2_error(postgres_repository):
    # Arrange
    with patch.object(postgres_repository, '_PostgresRepository__execute_query', side_effect=Psycopg2Error("DB error")):
        # Act
        outcome = postgres_repository.get_last_load_outcome()

    # Assert
    assert outcome == PostgresLastLoadOutcome.ERROR


# Verifica che il metodo get_last_load_outcome di PostgresRepository gestisca correttamente un'eccezione generica

def test_get_last_load_outcome_exception(postgres_repository):
    # Arrange
    with patch.object(postgres_repository, '_PostgresRepository__execute_query', side_effect=Exception("Unexpected error")):
        # Act
        with pytest.raises(Exception) as exc_info:
            postgres_repository.get_last_load_outcome()

        # Assert
        assert str(exc_info.value) == "Unexpected error"


# Verifica che il metodo get_messages di PostgresRepository gestisca correttamente il caso in cui non ci siano messaggi nel database

def test_get_messages_no_result(postgres_repository):
    # Arrange
    quantity = 5
    with patch.object(postgres_repository, '_PostgresRepository__execute_query', return_value=None):
        # Act
        messages = postgres_repository.get_messages(quantity)

    # Assert
    assert messages == []


# Verifica che il metodo get_last_load_outcome di PostgresRepository gestisca correttamente il caso in cui l'esito recuperato sia False

def test_get_last_load_outcome_false(postgres_repository):
    # Arrange
    with patch.object(postgres_repository, '_PostgresRepository__execute_query', return_value=(False,)):
        # Act
        outcome = postgres_repository.get_last_load_outcome()

    # Assert
    assert outcome == PostgresLastLoadOutcome.FALSE


# Verifica che il metodo execute_query di PostgresRepository gestisca correttamente le eccezioni

def test_execute_query_exception(postgres_repository, mock_conn):
    # Arrange
    query = "SELECT * FROM messages"
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.execute.side_effect = Exception("Unexpected error")

    # Act
    with pytest.raises(Exception) as exc_info:
        postgres_repository._PostgresRepository__execute_query(query)

    # Assert
    assert str(exc_info.value) == "Unexpected error"
    mock_cursor.execute.assert_called_once_with(query, ())


# Verifica che il metodo execute_query di PostgresRepository recuperi correttamente un singolo risultato per una query di lettura

def test_execute_query_fetch_one(postgres_repository, mock_conn):
    # Arrange
    query = "SELECT * FROM messages WHERE id = %s"
    params = (1,)
    expected_result = ("Message 1", datetime(2021, 10, 10, 10, 10, 1), PostgresMessageSender.USER.value)
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = expected_result

    # Act
    result = postgres_repository._PostgresRepository__execute_query(query, params, fetch_one=True)

    # Assert
    assert result == expected_result
    mock_cursor.execute.assert_called_once_with(query, params)
    mock_cursor.fetchone.assert_called_once()


# Verifica che il metodo execute_query di PostgresRepository recuperi correttamente tutti i risultati per una query di lettura

def test_execute_query_fetch_all(postgres_repository, mock_conn):
    # Arrange
    query = "SELECT * FROM messages"
    expected_result = [
        ("Message 1", datetime(2021, 10, 10, 10, 10, 1), PostgresMessageSender.USER.value),
        ("Message 2", datetime(2021, 10, 10, 10, 10, 2), PostgresMessageSender.CHATBOT.value)
    ]
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = expected_result

    # Act
    result = postgres_repository._PostgresRepository__execute_query(query, fetch_all=True)

    # Assert
    assert result == expected_result
    mock_cursor.execute.assert_called_once_with(query, ())
    mock_cursor.fetchall.assert_called_once()


# Verifica che il metodo execute_query di PostgresRepository esegua correttamente un commit per una query di scrittura

def test_execute_query_commit(postgres_repository, mock_conn):
    # Arrange
    query = "INSERT INTO messages (content, timestamp, sender) VALUES (%s, %s, %s)"
    params = ("Message 1", datetime(2021, 10, 10, 10, 10, 1), PostgresMessageSender.USER.value)
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    # Act
    postgres_repository._PostgresRepository__execute_query(query, params)

    # Assert
    mock_cursor.execute.assert_called_once_with(query, params)
    mock_conn.commit.assert_called_once()
