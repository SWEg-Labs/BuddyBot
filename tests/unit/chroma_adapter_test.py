import pytest
from unittest.mock import MagicMock
from datetime import datetime
import pytz
from freezegun import freeze_time

from models.document import Document
from models.question import Question
from entities.queryResultEntity import QueryResultEntity
from adapters.chromaVectorStoreAdapter import ChromaVectorStoreAdapter
from repositories.chromaVectorStoreRepository import ChromaVectorStoreRepository


# Verifica che il metodo load di ChromaVectorStoreAdapter gestisca correttamente le eccezioni

def test_load_exception():
    # Arrange
    mock_repository = MagicMock(spec=ChromaVectorStoreRepository)
    max_chunk_size = 41666
    adapter = ChromaVectorStoreAdapter(max_chunk_size, mock_repository)
    documents = [Document(page_content="doc1", metadata={"author": "Author1", "id": "1"})]
    mock_repository.load.side_effect = Exception("Load error")

    # Act
    with pytest.raises(Exception) as exc_info:
        adapter.load(documents)

    # Assert
    assert str(exc_info.value) == "Load error"


# Verifica che il metodo split di ChromaVectorStoreAdapter sollevi un'eccezione ValueError se un documento non ha un campo 'id' nei metadati

def test_split_value_error_missing_id():
    # Arrange
    mock_repository = MagicMock(spec=ChromaVectorStoreRepository)
    max_chunk_size = 41666
    adapter = ChromaVectorStoreAdapter(max_chunk_size, mock_repository)
    documents = [Document(page_content="doc1", metadata={"author": "Author1"})]  # Missing 'id'

    # Act
    with pytest.raises(ValueError) as exc_info:
        adapter._ChromaVectorStoreAdapter__split(documents)

    # Assert
    assert str(exc_info.value) == "Document metadata must contain an 'id' field."


# Verifica che il metodo split di ChromaVectorStoreAdapter inserisca correttamente la data di inserimento nel database vettoriale

@freeze_time("2025-03-01 12:00:00")
def test_split_vector_store_insertion_date():
    # Arrange
    mock_repository = MagicMock(spec=ChromaVectorStoreRepository)
    max_chunk_size = 41666
    adapter = ChromaVectorStoreAdapter(max_chunk_size, mock_repository)
    documents = [
        Document(page_content="doc1", metadata={"author": "Author1", "id": "1"}),
    ]

    # Act
    result = adapter._ChromaVectorStoreAdapter__split(documents)

    # Assert
    assert result[0].get_metadata()["vector_store_insertion_date"] == "2025-03-01 13:00:00"


# Verifica che il metodo split di ChromaVectorStoreAdapter gestisca correttamente i documenti con id duplicato

@freeze_time("2025-03-01 12:00:00")
def test_split_duplicate_documents():
    # Arrange
    mock_repository = MagicMock(spec=ChromaVectorStoreRepository)
    max_chunk_size = 41666
    adapter = ChromaVectorStoreAdapter(max_chunk_size, mock_repository)
    documents = [
        Document(page_content="doc1", metadata={"author": "Author1", "id": "1"}),
        Document(page_content="doc2", metadata={"author": "Author2", "id": "1"}),  # Duplicate ID
    ]

    # Act
    result = adapter._ChromaVectorStoreAdapter__split(documents)

    # Assert
    assert len(result) == 1  # Only one document should be processed


# Verifica che il metodo split di ChromaVectorStoreAdapter gestisca correttamente la conversione delle liste di file in stringhe

@freeze_time("2025-03-01 12:00:00")
def test_split_files_list_conversion():
    # Arrange
    mock_repository = MagicMock(spec=ChromaVectorStoreRepository)
    max_chunk_size = 41666
    adapter = ChromaVectorStoreAdapter(max_chunk_size, mock_repository)
    documents = [
        Document(page_content="doc1", metadata={"author": "Author1", "id": "1", "files": ["file1", "file2"]}),
    ]

    # Act
    result = adapter._ChromaVectorStoreAdapter__split(documents)

    # Assert
    assert result[0].get_metadata()["files"] == "file1\nfile2"


# Verifica che il metodo split di ChromaVectorStoreAdapter gestisca correttamente la formattazione delle date

@freeze_time("2025-03-01 12:00:00")
def test_split_date_formatting():
    # Arrange
    mock_repository = MagicMock(spec=ChromaVectorStoreRepository)
    max_chunk_size = 41666
    adapter = ChromaVectorStoreAdapter(max_chunk_size, mock_repository)
    italy_tz = pytz.timezone('Europe/Rome')
    documents = [
        Document(page_content="doc1", metadata={"author": "Author1", "id": "1", "date": italy_tz.localize(datetime(2025, 3, 1, 12, 0)), "creation_date": italy_tz.localize(datetime(2025, 3, 1, 12, 0))}),
    ]

    # Act
    result = adapter._ChromaVectorStoreAdapter__split(documents)

    # Assert
    assert result[0].get_metadata()["date"] == "2025-03-01 12:00:00"
    assert result[0].get_metadata()["creation_date"] == "2025-03-01 12:00:00"


# Verifica che il metodo similarity_search di ChromaVectorStoreAdapter gestisca correttamente le eccezioni

def test_similarity_search_exception():
    # Arrange
    mock_repository = MagicMock(spec=ChromaVectorStoreRepository)
    max_chunk_size = 41666
    adapter = ChromaVectorStoreAdapter(max_chunk_size, mock_repository)
    user_input = Question("test query")
    mock_repository.similarity_search.side_effect = Exception("Similarity search error")

    # Act
    with pytest.raises(Exception) as exc_info:
        adapter.similarity_search(user_input)

    # Assert
    assert str(exc_info.value) == "Similarity search error"


# Verifica che il metodo similarity_search di ChromaVectorStoreAdapter salti i documenti nulli

def test_similarity_search_skip_null_documents():
    # Arrange
    mock_repository = MagicMock(spec=ChromaVectorStoreRepository)
    max_chunk_size = 41666
    adapter = ChromaVectorStoreAdapter(max_chunk_size, mock_repository)
    user_input = Question("test query")
    query_result_entity = MagicMock(spec=QueryResultEntity)
    query_result_entity.get_documents.return_value = [[None, "doc2"]]
    query_result_entity.get_metadatas.return_value = [[{}, {}]]
    query_result_entity.get_distances.return_value = [[0.1, 0.2]]
    mock_repository.similarity_search.return_value = query_result_entity

    # Act
    result = adapter.similarity_search(user_input)

    # Assert
    assert len(result) == 1
    assert result[0].get_page_content() == "doc2"
    assert result[0].get_metadata()["distance"] == 0.2
