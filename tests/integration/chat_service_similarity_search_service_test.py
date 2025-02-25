from unittest.mock import MagicMock
from services.similaritySearchService import SimilaritySearchService
from services.chatService import ChatService
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document

def test_similarity_search_calls_repository():
    # Arrange
    mock_repository = MagicMock(spec=SimilaritySearchService)
    adapter = ChatService(mock_repository, MagicMock(spec=ChatOpenAI))
    user_input = "test query"
    mock_repository.similarity_search.return_value = [Document(page_content="Test content", metadata={"distance": 0.5})]
    
    # Act
    adapter.process_user_input(user_input)
    
    # Assert
    mock_repository.similarity_search.assert_called_once_with(user_input)

    # Devo estendere questo con anche la catena di LangChain, e solo allora potrò testare anche l'output
