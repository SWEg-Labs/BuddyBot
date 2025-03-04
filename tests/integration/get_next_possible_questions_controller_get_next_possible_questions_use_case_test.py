from unittest.mock import MagicMock

from models.quantity import Quantity
from models.questionAnswerCouple import QuestionAnswerCouple
from models.getNextPossibleQuestionsController import GetNextPossibleQuestionsController

# Verifica che il metodo get_next_possible_questions di GetNextPossibleQuestionsController chiami il metodo get_next_possible_questions di GetNextPossibleQuestionsUseCase

def test_get_next_possible_questions_calls_use_case_method():
    # Arrange
    mock_use_case = MagicMock()
    controller = GetNextPossibleQuestionsController(mock_use_case)

    question_answer_quantity = {
        "question": "test question",
        "answer": "test answer",
        "quantity": 3
    }

    question_answer_couple = QuestionAnswerCouple(question_answer_quantity["question"], question_answer_quantity["answer"])
    quantity = Quantity(question_answer_quantity["quantity"])

    expected_possible_questions = {
        "next_question_1": "some answer 1",
        "next_question_2": "some answer 2",
        "next_question_3": "some answer 3"
    }
    mock_use_case.get_next_possible_questions.return_value = expected_possible_questions

    # Act
    result = controller.get_next_possible_questions(question_answer_quantity)

    # Assert
    mock_use_case.get_next_possible_questions.assert_called_once_with(question_answer_couple, quantity)
    assert result == expected_possible_questions
