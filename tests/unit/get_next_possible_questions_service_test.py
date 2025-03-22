import pytest
from unittest.mock import MagicMock

from models.quantity import Quantity
from models.question import Question
from models.answer import Answer
from models.questionAnswerCouple import QuestionAnswerCouple
from models.header import Header
from services.getNextPossibleQuestionsService import GetNextPossibleQuestionsService
from ports.getNextPossibleQuestionsPort import GetNextPossibleQuestionsPort


# Verifica che il costruttore di GetNextPossibleQuestionsService sollevi un'eccezione se l'header non contiene la stringa '***quantity***'

def test_init_raises_exception_if_header_does_not_contain_quantity():
    # Arrange
    header = Header("test header without quantity")
    mock_port = MagicMock(spec=GetNextPossibleQuestionsPort)

    # Act
    with pytest.raises(ValueError) as exc_info:
        GetNextPossibleQuestionsService(header=header, get_next_possible_questions_port=mock_port)

    # Assert
    assert str(exc_info.value) == "Header does not contain '***quantity***'"


# Verifica che il metodo get_next_possible_questions di GetNextPossibleQuestionsService gestisca correttamente le eccezioni

def test_get_next_possible_questions_handles_exceptions():
    # Arrange
    header = Header("test header with ***quantity*** questions requested")
    mock_port = MagicMock(spec=GetNextPossibleQuestionsPort)
    service = GetNextPossibleQuestionsService(header=header, get_next_possible_questions_port=mock_port)

    question_answer_couple = QuestionAnswerCouple(
        Question("test question"),
        Answer("test answer")
    )
    quantity = Quantity(3)

    mock_port.get_next_possible_questions.side_effect = Exception("Port error")

    # Act
    with pytest.raises(Exception) as exc_info:
        service.get_next_possible_questions(question_answer_couple, quantity)

    # Assert
    assert str(exc_info.value) == "Port error"
