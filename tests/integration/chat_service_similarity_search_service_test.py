from unittest.mock import MagicMock
from services.similaritySearchService import SimilaritySearchService
from services.chatService import ChatService
from services.generateAnswerService import GenerateAnswerService
from business_data_classes.answer import Answer
from langchain_core.documents import Document

# Verifica che il metodo similarity_search di ChatService chiami il metodo similarity_search di SimilaritySearchService

def test_chat_service_calls_similarity_search_service():
    # Arrange
    mock_similarity_search_service = MagicMock(spec=SimilaritySearchService)
    mock_generate_answer_service = MagicMock(spec=GenerateAnswerService)
    chat_service = ChatService(mock_similarity_search_service, mock_generate_answer_service)
    user_input = "test query"
    documents = [Document(page_content="Test content", metadata={"distance": 0.5})]
    mock_similarity_search_service.similarity_search.return_value = documents
    mock_generate_answer_service.generate_answer.return_value = Answer("Test answer")
    
    # Act
    chat_service.process_user_input(user_input)
    
    # Assert
    mock_similarity_search_service.similarity_search.assert_called_once_with(user_input)

    # Non si può testare l'output perchè esso l'output della similarity_search viene passato al generate_answer_service,
    # e poi non viene restituito direttamente ma viene usato per creare un oggetto Answer che viene restituito.
    # Quindi non si può testare l'"output coincidente", bensì si può testare solo la "chiamata con il giusto input".
    # assert result == mock_documents

