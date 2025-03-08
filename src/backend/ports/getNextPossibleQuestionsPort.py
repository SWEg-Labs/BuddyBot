from abc import ABC, abstractmethod
from models.questionAnswerCouple import QuestionAnswerCouple
from models.header import Header
from models.nextPossibleQuestions import NextPossibleQuestions

class GetNextPossibleQuestionsPort(ABC):
    """
    Interface for retrieving the next possible questions based on a question-answer couple and header.
    """

    @abstractmethod
    def get_next_possible_questions(self, question_answer_couple: QuestionAnswerCouple, header: Header) -> NextPossibleQuestions:
        """
        Retrieves the next possible questions based on the provided question-answer couple and header.
        Args:
            question_answer_couple (QuestionAnswerCouple): The question-answer couple.
            header (Header): The header information.
        Returns:
            NextPossibleQuestions: The next possible questions.
        """
        pass
