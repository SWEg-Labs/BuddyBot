from abc import ABC, abstractmethod
from models.quantity import Quantity
from models.questionAnswerCouple import QuestionAnswerCouple
from models.nextPossibleQuestions import NextPossibleQuestions

class GetNextPossibleQuestionsUseCase(ABC):
    """
    Interface for the use case of retrieving the next possible questions.
    """

    @abstractmethod
    def get_next_possible_questions(self, question_answer_couple: QuestionAnswerCouple, quantity: Quantity) -> NextPossibleQuestions:
        """
        Retrieves the next possible questions based on the provided question-answer-quantity data.
        Args:
            question_answer_couple (QuestionAnswerCouple): The question-answer couple.
            quantity (Quantity): The quantity of next possible questions to retrieve.
        Returns:
            NextPossibleQuestions: The next possible questions.
        """
        pass
