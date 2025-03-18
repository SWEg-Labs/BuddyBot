import pytest
from unittest.mock import MagicMock
import requests
from requests.exceptions import ConnectTimeout

from entities.chromaDocumentEntity import ChromaDocumentEntity
from repositories.chromaVectorStoreRepository import ChromaVectorStoreRepository


# Verifica che il metodo load di ChromaVectorStoreRepository carichi correttamente i documenti nel database vettoriale

def test_load_success():
    # Arrange
    mock_collection = MagicMock()
    repository = ChromaVectorStoreRepository(mock_collection)
    documents = [
        MagicMock(spec=ChromaDocumentEntity),
        MagicMock(spec=ChromaDocumentEntity)
    ]
    for i, doc in enumerate(documents):
        doc.get_metadata.return_value = {"doc_id": str(i)}
        doc.get_page_content.return_value = f"content_{i}"

    # Act
    result = repository.load(documents)

    # Assert
    assert result.get_outcome() is True
    assert result.get_num_added_items() == 2
    assert result.get_num_modified_items() == 0
    assert result.get_num_deleted_items() == 0


# Verifica che il metodo load di ChromaVectorStoreRepository gestisca correttamente le eccezioni durante l'aggiunta dei documenti
# nel database vettoriale

def test_load_exception():
    # Arrange
    mock_collection = MagicMock()
    repository = ChromaVectorStoreRepository(mock_collection)
    documents = [MagicMock(spec=ChromaDocumentEntity)]
    documents[0].get_metadata.return_value = {"doc_id": "1"}
    documents[0].get_page_content.return_value = "content_1"
    mock_collection.add.side_effect = ConnectTimeout("Load error")

    # Act
    result = repository.load(documents)

    # Assert
    assert result.get_outcome() is False
    assert result.get_num_added_items() == 0
    assert result.get_num_modified_items() == 0
    assert result.get_num_deleted_items() == 0


# Verifica che il metodo load di ChromaVectorStoreRepository gestisca correttamente le eccezioni durante la preparazione dei dati
# per l'aggiunta nel database vettoriale

def test_load_exception_preparing_new_data():
    # Arrange
    mock_collection = MagicMock()
    repository = ChromaVectorStoreRepository(mock_collection)
    documents = [MagicMock(spec=ChromaDocumentEntity)]
    documents[0].get_metadata.side_effect = Exception("Metadata error")

    # Act
    with pytest.raises(Exception) as exc_info:
        repository.load(documents)

    # Assert
    assert str(exc_info.value) == "Metadata error"


# Verifica che il metodo load di ChromaVectorStoreRepository gestisca correttamente le eccezioni durante il recupero dei vecchi dati
# dal database vettoriale

def test_load_exception_fetching_old_data():
    # Arrange
    mock_collection = MagicMock()
    mock_collection.get.side_effect = requests.exceptions.ConnectTimeout("Fetch error")
    repository = ChromaVectorStoreRepository(mock_collection)
    documents = [MagicMock(spec=ChromaDocumentEntity)]
    documents[0].get_metadata.return_value = {"doc_id": "1"}
    documents[0].get_page_content.return_value = "content_1"

    # Act
    result = repository.load(documents)

    # Assert
    assert result.get_outcome() is False
    assert result.get_num_added_items() == 0
    assert result.get_num_modified_items() == 0
    assert result.get_num_deleted_items() == 0


# Verifica che il metodo load di ChromaVectorStoreRepository gestisca correttamente le eccezioni durante il parsing delle date
# per documenti non di tipo GitHub File

def test_load_exception_parsing_datetime_non_github_file():
    # Arrange
    mock_collection = MagicMock()
    repository = ChromaVectorStoreRepository(mock_collection)
    documents = [MagicMock(spec=ChromaDocumentEntity)]
    documents[0].get_metadata.return_value = {
        "doc_id": "1",
        "item_type": "Non-GitHub File",
        "last_update": "2023-01-01 00:00:00",
    }
    documents[0].get_page_content.return_value = "content_1"
    mock_collection.get.return_value = {
        "ids": ["1"],
        "metadatas": [{"last_update": "invalid_date"}],
    }

    # Act
    with pytest.raises(Exception) as exc_info:
        repository.load(documents)

    # Assert
    assert str(exc_info.value) == "time data 'invalid_date' does not match format '%Y-%m-%d %H:%M:%S'"


# Verifica che il metodo load di ChromaVectorStoreRepository gestisca correttamente le eccezioni durante il parsing delle date
# per documenti di tipo GitHub File

def test_load_exception_parsing_dates_github_file():
    # Arrange
    mock_collection = MagicMock()
    repository = ChromaVectorStoreRepository(mock_collection)
    documents = [MagicMock(spec=ChromaDocumentEntity)]
    documents[0].get_metadata.return_value = {
        "doc_id": "sha-1",
        "item_type": "GitHub File",
        "creation_date": "2023-01-01 00:00:00",
        "path": "/path/to/file",
    }
    documents[0].get_page_content.return_value = "content_1"
    mock_collection.get.return_value = {
        "ids": ["sha-2"],
        "metadatas": [{"item_type": "GitHub File", "path": "/path/to/file", "vector_store_insertion_date": "invalid_date"}],
    }

    # Act
    with pytest.raises(Exception) as exc_info:
        repository.load(documents)

    # Assert
    assert str(exc_info.value) == "time data 'invalid_date' does not match format '%Y-%m-%d %H:%M:%S'"


# Verifica che il metodo load di ChromaVectorStoreRepository gestisca correttamente l'eccezione riguardante un documento
# di tipo GitHub File senza il campo 'path'

def test_load_missing_path_field_in_github_file():
    # Arrange
    mock_collection = MagicMock()
    repository = ChromaVectorStoreRepository(mock_collection)
    documents = [MagicMock(spec=ChromaDocumentEntity)]
    documents[0].get_metadata.return_value = {"doc_id": "1", "item_type": "GitHub File"}
    documents[0].get_page_content.return_value = "content_1"

    # Act
    with pytest.raises(Exception) as exc_info:
        repository.load(documents)

    # Assert
    assert str(exc_info.value) == "Missing 'path' field in metadata for GitHub File with doc_id 1"


# Verifica che il metodo load di ChromaVectorStoreRepository segnali correttamente la modifica di un documento di tipo GitHub File,
# e non la sua creazione, se la data di creazione è più vecchia di quella dell'ultimo inserimento nel database vettoriale

def test_load_github_file_modification_based_on_dates():
    # Arrange
    mock_collection = MagicMock()
    repository = ChromaVectorStoreRepository(mock_collection)
    documents = [MagicMock(spec=ChromaDocumentEntity)]
    documents[0].get_metadata.return_value = {
        "doc_id": "1",
        "item_type": "GitHub File",
        "creation_date": "2023-01-01 00:00:00",
        "path": "/path/to/file",
    }
    documents[0].get_page_content.return_value = "content_1"
    mock_collection.get.return_value = {
        "ids": ["2"],
        "metadatas": [{"item_type": "GitHub File", "path": "/path/to/file", "vector_store_insertion_date": "2023-01-02 00:00:00"}],
    }

    # Act
    result = repository.load(documents)

    # Assert
    assert result.get_outcome() is True
    assert result.get_num_added_items() == 0
    assert result.get_num_modified_items() == 1
    assert result.get_num_deleted_items() == 0


# Verifica che il metodo load di ChromaVectorStoreRepository ignori i documenti di tipo GitHub File durante il controllo
# di modifica basato sul metadato 'last_update'

def test_load_skip_github_file_during_update_check():
    # Arrange
    mock_collection = MagicMock()
    repository = ChromaVectorStoreRepository(mock_collection)
    documents = [MagicMock(spec=ChromaDocumentEntity)]
    documents[0].get_metadata.return_value = {"doc_id": "1", "item_type": "GitHub File", "last_update": "2023-01-01 00:00:00"}
    documents[0].get_page_content.return_value = "content_1"
    mock_collection.get.return_value = {"ids": ["1"], "metadatas": [{"last_update": "2023-01-01 00:00:00"}]}

    # Act
    result = repository.load(documents)

    # Assert
    assert result.get_outcome() is True
    assert result.get_num_added_items() == 0
    assert result.get_num_modified_items() == 0
    assert result.get_num_deleted_items() == 0


# Verifica che il metodo load di ChromaVectorStoreRepository segnali correttamente la modifica di un documento con il metadato
# 'last_update' più recente rispetto al corrispondente presente nel database vettoriale

def test_load_update_document_with_recent_last_update():
    # Arrange
    mock_collection = MagicMock()
    repository = ChromaVectorStoreRepository(mock_collection)
    documents = [MagicMock(spec=ChromaDocumentEntity)]
    documents[0].get_metadata.return_value = {"doc_id": "1", "last_update": "2023-01-02 00:00:00"}
    documents[0].get_page_content.return_value = "content_1"
    mock_collection.get.return_value = {"ids": ["1"], "metadatas": [{"last_update": "2023-01-01 00:00:00"}]}

    # Act
    result = repository.load(documents)

    # Assert
    assert result.get_outcome() is True
    assert result.get_num_added_items() == 0
    assert result.get_num_modified_items() == 1
    assert result.get_num_deleted_items() == 0


# Verifica che il metodo load di ChromaVectorStoreRepository gestisca correttamente le eccezioni durante la cancellazione dei documenti
# dal database vettoriale

def test_load_exception_while_deleting_documents():
    # Arrange
    mock_collection = MagicMock()
    repository = ChromaVectorStoreRepository(mock_collection)
    documents = [MagicMock(spec=ChromaDocumentEntity)]
    documents[0].get_metadata.return_value = {"doc_id": "1"}
    documents[0].get_page_content.return_value = "content_1"
    mock_collection.get.return_value = {"ids": ["2"], "metadatas": [{}]}
    mock_collection.delete.side_effect = ConnectTimeout("Delete error")

    # Act
    result = repository.load(documents)

    # Assert
    assert result.get_outcome() is False
    assert result.get_num_added_items() == 0
    assert result.get_num_modified_items() == 0
    assert result.get_num_deleted_items() == 0


# Verifica che il metodo similarity_search di ChromaVectorStoreRepository restituisca correttamente i risultati della ricerca di similarità

def test_similarity_search_success():
    # Arrange
    mock_collection = MagicMock()
    repository = ChromaVectorStoreRepository(mock_collection)
    query = "test query"
    mock_collection.query.return_value = {
        "documents": ["doc1", "doc2"],
        "metadatas": [{"id": "1"}, {"id": "2"}],
        "distances": [0.1, 0.2]
    }

    # Act
    result = repository.similarity_search(query)

    # Assert
    assert len(result.get_documents()) == 2
    assert result.get_documents() == ["doc1", "doc2"]
    assert result.get_metadatas() == [{"id": "1"}, {"id": "2"}]
    assert result.get_distances() == [0.1, 0.2]


# Verifica che il metodo similarity_search di ChromaVectorStoreRepository gestisca correttamente le eccezioni

def test_similarity_search_exception():
    # Arrange
    mock_collection = MagicMock()
    repository = ChromaVectorStoreRepository(mock_collection)
    query = "test query"
    mock_collection.query.side_effect = Exception("Search error")

    # Act
    with pytest.raises(Exception) as exc_info:
        repository.similarity_search(query)

    # Assert
    assert str(exc_info.value) == "Search error"
