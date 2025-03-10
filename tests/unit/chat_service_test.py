import pytest
from unittest.mock import Mock

from models.question import Question
from models.answer import Answer
from models.document import Document
from services.similaritySearchService import SimilaritySearchService
from services.generateAnswerService import GenerateAnswerService
from use_cases.chatUseCase import ChatUseCase
from services.chatService import ChatService


@pytest.fixture
def mock_similarity_search_service():
    return Mock(spec=SimilaritySearchService)

@pytest.fixture
def mock_generate_answer_service():
    return Mock(spec=GenerateAnswerService)

@pytest.fixture
def chat_service(mock_similarity_search_service, mock_generate_answer_service):
    return ChatService(mock_similarity_search_service, mock_generate_answer_service)


# Verifica che il metodo get_answer di ChatService restituisca la risposta corretta

def test_get_answer(chat_service, mock_similarity_search_service, mock_generate_answer_service):
    # Arrange
    user_input = Question("What is AI?")
    relevant_docs = [Document("AI is the simulation of human intelligence in machines.")]
    expected_answer = Answer("AI is the simulation of human intelligence in machines.")

    mock_similarity_search_service.similarity_search.return_value = relevant_docs
    mock_generate_answer_service.generate_answer.return_value = expected_answer

    # Act
    answer = chat_service.get_answer(user_input)

    # Assert
    assert answer == expected_answer
    mock_similarity_search_service.similarity_search.assert_called_once_with(user_input)
    mock_generate_answer_service.generate_answer.assert_called_once_with(user_input, relevant_docs)


# Verifica che il metodo get_answer di ChatService gestisca correttamente le eccezioni

def test_get_answer_Exception(chat_service, mock_similarity_search_service, mock_generate_answer_service):
    # Arrange
    user_input = Question("What is AI?")
    mock_similarity_search_service.similarity_search.side_effect = Exception("Similarity search error")

    # Act
    with pytest.raises(Exception, match="Similarity search error"):
        chat_service.get_answer(user_input)

    # Assert
    mock_similarity_search_service.similarity_search.assert_called_once_with(user_input)
    mock_generate_answer_service.generate_answer.assert_not_called()


# Verifica che il metodo similarity_search di ChatService gestisca correttamente le eccezioni

def test_similarity_search_Exception(chat_service, mock_similarity_search_service):
    # Arrange
    user_input = Question("What is AI?")
    mock_similarity_search_service.similarity_search.side_effect = Exception("Similarity search error")

    # Act
    with pytest.raises(Exception, match="Similarity search error"):
        chat_service.similarity_search(user_input)

    # Assert
    mock_similarity_search_service.similarity_search.assert_called_once_with(user_input)


# Verifica che il metodo generate_answer di ChatService gestisca correttamente le eccezioni

def test_generate_answer_Exception(chat_service, mock_generate_answer_service):
    # Arrange
    user_input = Question("What is AI?")
    relevant_docs = [Document("AI is the simulation of human intelligence in machines.")]
    mock_generate_answer_service.generate_answer.side_effect = Exception("Generate answer error")

    # Act
    with pytest.raises(Exception, match="Generate answer error"):
        chat_service.generate_answer(user_input, relevant_docs)

    # Assert
    mock_generate_answer_service.generate_answer.assert_called_once_with(user_input, relevant_docs)
