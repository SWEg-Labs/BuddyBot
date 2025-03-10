from typing import Dict, Union

from models.question import Question
from models.answer import Answer
from models.quantity import Quantity
from models.questionAnswerCouple import QuestionAnswerCouple
from models.nextPossibleQuestions import NextPossibleQuestions
from use_cases.getNextPossibleQuestionsUseCase import GetNextPossibleQuestionsUseCase
from utils.logger import logger

class GetNextPossibleQuestionsController:
    """
    Controller for handling the retrieval of the next possible questions based on the provided question-answer-quantity data.
    Attributes:
        get_next_possible_questions_use_case (GetNextPossibleQuestionsUseCase): The use case for getting the next possible questions.
    """

    def __init__(self, get_next_possible_questions_use_case: GetNextPossibleQuestionsUseCase):
        """
        Initializes the GetNextPossibleQuestionsController with the provided use case.
        Args:
            get_next_possible_questions_use_case (GetNextPossibleQuestionsUseCase): The use case for getting the next possible questions.
        Raises:
            Exception: If there is an error during initialization.
        """
        try:
            self.__get_next_possible_questions_use_case = get_next_possible_questions_use_case
        except Exception as e:
            logger.error(f"Error initializing GetNextPossibleQuestionsController: {e}")
            raise e

    def get_next_possible_questions(self, question_answer_quantity: Dict[str, Union[str, int]]) -> Dict[str, str]:
        """
        Retrieves the next possible questions based on the provided question-answer-quantity data.
        Args:
            question_answer_quantity (Dict[str, Union[str, int]]): A dictionary containing the question, answer, and quantity.
        Returns:
            Dict[str, str]: A dictionary of the next possible questions.
        Raises:
            Exception: If there is an error during the retrieval process.
        """
        try:
            question = Question(question_answer_quantity["question"])
            answer = Answer(question_answer_quantity["answer"])
            quantity = Quantity(question_answer_quantity["quantity"])
            question_answer_couple = QuestionAnswerCouple(question, answer)

            next_possible_questions_object = self.__get_next_possible_questions_use_case.get_next_possible_questions(question_answer_couple, quantity)

            possible_questions = next_possible_questions_object.get_possible_questions()
            next_possible_questions_dict = {
                f"question {i + 1}": possible_question.get_content()
                for i, possible_question in enumerate(possible_questions)
            }

            message = "Next possible questions retrieved successfully: " + ", ".join(
                [f"{key}: {value}" for key, value in next_possible_questions_dict.items()]
            )
            logger.info(message)

            return next_possible_questions_dict
        except Exception as e:
            logger.error(f"Error in GetNextPossibleQuestionsController: {e}")
            raise e
