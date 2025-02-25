from unittest.mock import MagicMock
from services.similaritySearchService import SimilaritySearchService
from services.chatService import ChatService
from services.generateAnswerService import GenerateAnswerService
from business_data_classes.answer import Answer
from langchain_core.documents import Document

# Verifica che il metodo generate_answer di ChatService chiami il metodo generate_answer di GenerateAnswerService

def test_chat_service_calls_generate_answer_service():
    # Arrange
    mock_similarity_search_service = MagicMock(spec=SimilaritySearchService)
    mock_generate_answer_service = MagicMock(spec=GenerateAnswerService)
    chat_service = ChatService(mock_similarity_search_service, mock_generate_answer_service)
    user_input = "test query"
    mock_similarity_search_service.similarity_search.return_value = [Document(page_content="Test content", metadata={"distance": 0.5})]
    answer = Answer("Test answer")
    mock_generate_answer_service.generate_answer.return_value = answer
    
    # Act
    result = chat_service.process_user_input(user_input)
    
    # Assert
    mock_generate_answer_service.generate_answer.assert_called_once_with([Document(page_content="Test content", metadata={"distance": 0.5})])
    assert result == answer