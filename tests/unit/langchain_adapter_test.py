import pytest
from unittest.mock import MagicMock

from models.document import Document
from models.question import Question
from models.header import Header
from models.answer import Answer
from models.questionAnswerCouple import QuestionAnswerCouple
from adapters.langChainAdapter import LangChainAdapter
from repositories.langChainRepository import LangChainRepository


# Verifica che il metodo generate_answer di LangChainAdapter gestisca il superamento del limite di token
# escludendo i documenti che lo fanno superare

def test_generate_answer_token_limit_exceeded():
    # Arrange
    max_num_tokens = 10
    mock_langchain_repository = MagicMock(spec=LangChainRepository)
    langchain_adapter = LangChainAdapter(max_num_tokens, mock_langchain_repository)
    user_input = Question("test question")
    relevant_docs = [
        Document(page_content="doc1", metadata={"distance": 0.5}),
        Document(page_content="doc2", metadata={"distance": 0.75}),
    ]
    header = Header("test header")
    mock_langchain_repository.generate_answer.return_value = "test answer"

    # Act
    result = langchain_adapter.generate_answer(user_input, relevant_docs, header)

    # Assert
    assert len(result.get_content()) > 0  # Ensure an answer is generated even if token limit is exceeded


# Verifica che il metodo generate_answer di LangChainAdapter gestisca correttamente le eccezioni

def test_generate_answer_exception():
    # Arrange
    max_num_tokens = 128000
    mock_langchain_repository = MagicMock(spec=LangChainRepository)
    langchain_adapter = LangChainAdapter(max_num_tokens, mock_langchain_repository)
    user_input = Question("test question")
    relevant_docs = [
        Document(page_content="doc1", metadata={"distance": 0.5}),
        Document(page_content="doc2", metadata={"distance": 0.75}),
    ]
    header = Header("test header")
    mock_langchain_repository.generate_answer.side_effect = Exception("Repository error")

    # Act
    with pytest.raises(Exception) as exc_info:
        langchain_adapter.generate_answer(user_input, relevant_docs, header)

    # Assert
    assert str(exc_info.value) == "Repository error"


# Verifica che il metodo get_next_possible_questions di LangChainAdapter gestisca correttamente le eccezioni

def test_get_next_possible_questions_exception():
    # Arrange
    max_num_tokens = 128000
    mock_langchain_repository = MagicMock(spec=LangChainRepository)
    langchain_adapter = LangChainAdapter(max_num_tokens, mock_langchain_repository)

    question = Question("test question")
    answer = Answer("test answer")
    question_answer_couple = QuestionAnswerCouple(question, answer)
    header = Header("test header")

    mock_langchain_repository.get_next_possible_questions.side_effect = Exception("Repository error")

    # Act
    with pytest.raises(Exception) as exc_info:
        langchain_adapter.get_next_possible_questions(question_answer_couple, header)

    # Assert
    assert str(exc_info.value) == "Repository error"
