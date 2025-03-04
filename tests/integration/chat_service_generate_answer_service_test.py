from unittest.mock import MagicMock
from services.similaritySearchService import SimilaritySearchService
from services.chatService import ChatService
from services.generateAnswerService import GenerateAnswerService
from models.question import Question
from models.answer import Answer
from models.document import Document

# Verifica che il metodo generate_answer di ChatService chiami il metodo generate_answer di GenerateAnswerService

def test_chat_service_calls_generate_answer_service():
    # Arrange
    mock_similarity_search_service = MagicMock(spec=SimilaritySearchService)
    mock_generate_answer_service = MagicMock(spec=GenerateAnswerService)
    chat_service = ChatService(mock_similarity_search_service, mock_generate_answer_service)
    user_input = Question("test query")
    relevant_docs = [
        Document(page_content="doc1"),
        Document(page_content="doc2"),
    ]
    answer = Answer("Test answer")
    mock_generate_answer_service.generate_answer.return_value = answer
    
    # Act
    result = chat_service.generate_answer(user_input, relevant_docs)
    
    # Assert
    mock_generate_answer_service.generate_answer.assert_called_once_with(user_input, relevant_docs)
    assert result == answer