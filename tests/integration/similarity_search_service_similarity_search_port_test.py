from unittest.mock import MagicMock
from langchain_core.documents import Document
from services.similaritySearchService import SimilaritySearchService
from ports.similaritySearchPort import SimilaritySearchPort

def test_similarity_search_calls_port_method():
    # Arrange
    mock_similarity_search_port = MagicMock(spec=SimilaritySearchPort)
    similarity_search_service = SimilaritySearchService(mock_similarity_search_port)
    user_input = "test input"
    mock_documents = [
        Document(page_content="doc1", metadata={"distance": 0.5}),
        Document(page_content="doc2", metadata={"distance": 0.75}),
    ]
    mock_similarity_search_port.similarity_search.return_value = mock_documents

    # Act
    result = similarity_search_service.similarity_search(user_input)

    # Assert
    mock_similarity_search_port.similarity_search.assert_called_once_with(user_input)
    assert result == mock_documents[:2]  # Assuming the threshold and gap conditions are met
