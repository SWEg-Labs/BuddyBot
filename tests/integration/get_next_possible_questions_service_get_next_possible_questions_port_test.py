from unittest.mock import MagicMock

from models.quantity import Quantity
from models.question import Question
from models.answer import Answer
from models.questionAnswerCouple import QuestionAnswerCouple
from models.nextPossibleQuestions import NextPossibleQuestions
from models.possibleQuestion import PossibleQuestion
from models.header import Header
from services.getNextPossibleQuestionsService import GetNextPossibleQuestionsService
from ports.getNextPossibleQuestionsPort import GetNextPossibleQuestionsPort

# Verifica che il metodo get_next_possible_questions di GetNextPossibleQuestionsService chiami il metodo get_next_possible_questions di GetNextPossibleQuestionsPort

def test_get_next_possible_questions_calls_port_method():
    # Arrange
    mock_port = MagicMock(spec=GetNextPossibleQuestionsPort)
    service = GetNextPossibleQuestionsService(get_next_possible_questions_port=mock_port)

    # Creazione degli input di test
    question_answer_couple = QuestionAnswerCouple(
        Question("test question"),
        Answer("test answer")
    )
    quantity = Quantity(3)

    header = Header(f"test header with {quantity.get_value()} questions requested")

    expected_possible_questions = NextPossibleQuestions(
        quantity=3,
        possible_questions = [
            PossibleQuestion("next_question_1"),
            PossibleQuestion("next_question_2"),
            PossibleQuestion("next_question_3")
        ],
    )
    mock_port.get_next_possible_questions.return_value = expected_possible_questions

    # Act
    result = service.get_next_possible_questions(question_answer_couple, quantity)

    # Assert
    mock_port.get_next_possible_questions.assert_called_once_with(question_answer_couple, header)
    assert result == expected_possible_questions
