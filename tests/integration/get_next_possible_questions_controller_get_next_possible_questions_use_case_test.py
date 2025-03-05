from unittest.mock import MagicMock

from models.quantity import Quantity
from models.question import Question
from models.answer import Answer
from models.questionAnswerCouple import QuestionAnswerCouple
from models.nextPossibleQuestions import NextPossibleQuestions
from models.possibleQuestion import PossibleQuestion
from controllers.getNextPossibleQuestionsController import GetNextPossibleQuestionsController
from use_cases.getNextPossibleQuestionsUseCase import GetNextPossibleQuestionsUseCase

# Verifica che il metodo get_next_possible_questions di GetNextPossibleQuestionsController chiami il metodo get_next_possible_questions di GetNextPossibleQuestionsUseCase

def test_get_next_possible_questions_calls_use_case_method():
    # Arrange
    mock_use_case = MagicMock(spec=GetNextPossibleQuestionsUseCase)
    controller = GetNextPossibleQuestionsController(mock_use_case)

    question_answer_quantity = {
        "question": "test question",
        "answer": "test answer",
        "quantity": 3
    }

    question_answer_couple = QuestionAnswerCouple(
        Question(question_answer_quantity["question"]),
        Answer(question_answer_quantity["answer"])
    )
    quantity = Quantity(question_answer_quantity["quantity"])

    expected_possible_questions = NextPossibleQuestions(
        quantity=3,
        possible_questions = [
            PossibleQuestion("next_question_1"),
            PossibleQuestion("next_question_2"),
            PossibleQuestion("next_question_3")
        ],
    )
    mock_use_case.get_next_possible_questions.return_value = expected_possible_questions

    # Act
    result = controller.get_next_possible_questions(question_answer_quantity)

    # Assert
    mock_use_case.get_next_possible_questions.assert_called_once_with(question_answer_couple, quantity)
    assert result == expected_possible_questions
