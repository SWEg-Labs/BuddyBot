import pytest
from unittest.mock import MagicMock, patch
from langchain_openai import ChatOpenAI

from entities.langChainDocumentEntity import LangChainDocumentEntity
from repositories.langChainRepository import LangChainRepository


# Verifica che il metodo generate_answer di LangChainRepository generi correttamente una risposta

def test_generate_answer_generates_correct_response():
    # Arrange
    mock_llm = MagicMock(spec=ChatOpenAI)
    repository = LangChainRepository(mock_llm)
    user_input = "test question"
    relevant_docs = [
        LangChainDocumentEntity(page_content="doc1", metadata={"distance": 0.5}),
        LangChainDocumentEntity(page_content="doc2", metadata={"distance": 0.75}),
    ]
    header = "test header"
    expected_response = "test answer"
    mock_llm.invoke.return_value = expected_response

    # Act
    response = repository.generate_answer(user_input, relevant_docs, header)

    # Assert
    assert response == expected_response


# Verifica che il metodo generate_answer di LangChainRepository gestisca correttamente le eccezioni

def test_generate_answer_handles_exceptions():
    # Arrange
    mock_llm = MagicMock(spec=ChatOpenAI)
    repository = LangChainRepository(mock_llm)
    user_input = "test question"
    relevant_docs = [
        LangChainDocumentEntity(page_content="doc1", metadata={"distance": 0.5}),
        LangChainDocumentEntity(page_content="doc2", metadata={"distance": 0.75}),
    ]
    header = "test header"
    mock_llm.invoke.side_effect = Exception("Test exception")

    # Act
    with pytest.raises(Exception) as exc_info:
        repository.generate_answer(user_input, relevant_docs, header)

    # Assert
    assert str(exc_info.value) == "Test exception"


# Verifica che il metodo get_next_possible_questions di LangChainRepository generi correttamente le prossime domande possibili

def test_get_next_possible_questions_generates_correct_response():
    # Arrange
    mock_llm = MagicMock(spec=ChatOpenAI)
    repository = LangChainRepository(mock_llm)
    question_answer_couple = [
        LangChainDocumentEntity(page_content="test question"),
        LangChainDocumentEntity(page_content="test answer"),
    ]
    header = "test header"
    expected_response = "next possible questions"
    mock_llm.invoke.return_value = expected_response

    # Act
    response = repository.get_next_possible_questions(question_answer_couple, header)

    # Assert
    assert response == expected_response


# Verifica che il metodo get_next_possible_questions di LangChainRepository gestisca correttamente le eccezioni

def test_get_next_possible_questions_handles_exceptions():
    # Arrange
    mock_llm = MagicMock(spec=ChatOpenAI)
    repository = LangChainRepository(mock_llm)
    question_answer_couple = [
        LangChainDocumentEntity(page_content="test question"),
        LangChainDocumentEntity(page_content="test answer"),
    ]
    header = "test header"
    mock_llm.invoke.side_effect = Exception("Test exception")

    # Act
    with pytest.raises(Exception) as exc_info:
        repository.get_next_possible_questions(question_answer_couple, header)

    # Assert
    assert str(exc_info.value) == "Test exception"
