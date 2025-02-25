from unittest.mock import MagicMock
from langchain_core.documents import Document
from adapters.chromaVectorStoreAdapter import ChromaVectorStoreAdapter
from repositories.chromaVectorStoreRepository import ChromaVectorStoreRepository

# Verifica che il metodo similarity_search di ChromaVectorStoreAdapter chiami il metodo similarity_search di ChromaVectorStoreRepository

def test_similarity_search_calls_repository():
    # Arrange
    mock_repository = MagicMock(spec=ChromaVectorStoreRepository)
    adapter = ChromaVectorStoreAdapter(mock_repository)
    user_input = "test query"
    documents = [
        Document(page_content="doc1", metadata={"distance": 0.5}),
        Document(page_content="doc2", metadata={"distance": 0.75}),
    ]
    mock_repository.similarity_search.return_value = {
        'documents': [["doc1", "doc2"]],
        'metadatas': [[{"distance": 0.5}, {"distance": 0.75}]],
        'distances': [[0.5, 0.75]]
    }

    # Act
    result = adapter.similarity_search(user_input)

    # Assert
    mock_repository.similarity_search.assert_called_once_with(user_input)
    assert result == documents
