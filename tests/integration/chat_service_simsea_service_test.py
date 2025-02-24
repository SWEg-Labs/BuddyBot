import pytest
from unittest.mock import MagicMock
from services.similaritySearchService import SimilaritySearchService
from services.chatService import ChatService
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document

@pytest.fixture
def mock_similarity_search_service():
    return MagicMock(spec=SimilaritySearchService)

@pytest.fixture
def mock_llm():
    return MagicMock(spec=ChatOpenAI)

@pytest.fixture
def chat_service(mock_llm, mock_similarity_search_service):
    return ChatService(mock_llm, mock_similarity_search_service)

def test_process_user_input_calls_similarity_search(chat_service, mock_similarity_search_service):
    user_input = "Test input"
    mock_similarity_search_service.similarity_search.return_value = [Document(page_content="Test content", metadata={"distance": 0.5})]

    chat_service.process_user_input(user_input)

    mock_similarity_search_service.similarity_search.assert_called_once_with(user_input)
