from unittest.mock import MagicMock
from services.similaritySearchService import SimilaritySearchService
from services.chatService import ChatService
from services.generateAnswerService import GenerateAnswerService
from models.question import Question
from models.document import Document


# Verifica che il metodo similarity_search di ChatService chiami il metodo similarity_search di SimilaritySearchService

def test_chat_service_calls_similarity_search_service():
    # Arrange
    mock_similarity_search_service = MagicMock(spec=SimilaritySearchService)
    mock_generate_answer_service = MagicMock(spec=GenerateAnswerService)
    chat_service = ChatService(mock_similarity_search_service, mock_generate_answer_service)
    user_input = Question("test query")
    relevant_docs = [Document(page_content="Test content", metadata={"distance": 0.5})]
    mock_similarity_search_service.similarity_search.return_value = relevant_docs
    
    # Act
    result = chat_service.similarity_search(user_input)
    
    # Assert
    mock_similarity_search_service.similarity_search.assert_called_once_with(user_input)
    assert result == relevant_docs

