import pytest
from unittest.mock import MagicMock

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


# Verifica che il metodo load di ChromaVectorStoreRepository gestisca correttamente le eccezioni

def test_load_exception():
    # Arrange
    mock_collection = MagicMock()
    repository = ChromaVectorStoreRepository(mock_collection)
    documents = [MagicMock(spec=ChromaDocumentEntity)]
    documents[0].get_metadata.return_value = {"doc_id": "1"}
    documents[0].get_page_content.return_value = "content_1"
    mock_collection.add.side_effect = Exception("Load error")

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
