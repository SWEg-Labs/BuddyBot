from unittest.mock import MagicMock
from models.document import Document
from models.question import Question
from services.similaritySearchService import SimilaritySearchService
from ports.similaritySearchPort import SimilaritySearchPort

# Verifica che il metodo similarity_search di SimilaritySearchService chiami il metodo similarity_search di SimilaritySearchPort

def test_similarity_search_calls_port_method():
    # Arrange
    mock_similarity_search_port = MagicMock(spec=SimilaritySearchPort)
    similarity_search_service = SimilaritySearchService(mock_similarity_search_port)
    user_input = Question("test input")
    documents = [
        Document(page_content="doc1", metadata={"distance": 0.5}),
        Document(page_content="doc2", metadata={"distance": 0.75}),
    ]
    mock_similarity_search_port.similarity_search.return_value = documents

    # Act
    result = similarity_search_service.similarity_search(user_input)

    # Assert
    mock_similarity_search_port.similarity_search.assert_called_once_with(user_input)
    assert result == documents[:2]  # Assuming the threshold and gap conditions are met
