from models.quantity import Quantity
from models.questionAnswerCouple import QuestionAnswerCouple
from models.nextPossibleQuestions import NextPossibleQuestions
from models.header import Header
from use_cases.getNextPossibleQuestionsUseCase import GetNextPossibleQuestionsUseCase
from ports.getNextPossibleQuestionsPort import GetNextPossibleQuestionsPort
from utils.logger import logger
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
class GetNextPossibleQuestionsService(GetNextPossibleQuestionsUseCase):
    """
    Service for handling the retrieval of the next possible questions based on the provided question-answer-quantity data.
    Attributes:
        header (Header): The header for the service.
        get_next_possible_questions_port (GetNextPossibleQuestionsPort): The port for getting the next possible questions.
    """

    def __init__(self, header: Header, get_next_possible_questions_port: GetNextPossibleQuestionsPort):
        """
        Initializes the GetNextPossibleQuestionsService with the provided port.
        Args:
            header (Header): The header for the service.
            get_next_possible_questions_port (GetNextPossibleQuestionsPort): The port for getting the next possible questions.
        Raises:
            Exception: If there is an error during initialization.
        """
        try:
            self.__header = header
            self.__get_next_possible_questions_port = get_next_possible_questions_port
        except Exception as e:
            logger.error(f"Error initializing GetNextPossibleQuestionsService: {e}")
            raise e

    def get_next_possible_questions(self, question_answer_couple: QuestionAnswerCouple, quantity: Quantity) -> NextPossibleQuestions:
        """
        Retrieves the next possible questions based on the provided question-answer-quantity data.
        Args:
            question_answer_couple (QuestionAnswerCouple): The question-answer couple.
            quantity (Quantity): The quantity of next possible questions to retrieve.
        Returns:
            NextPossibleQuestions: The next possible questions.
        Raises:
            Exception: If there is an error during the retrieval process.
        """
        try:
            header_content = self.__header.get_content().replace("***quantity***", str(quantity.get_value()))
            header = Header(header_content)
            return self.__get_next_possible_questions_port.get_next_possible_questions(question_answer_couple, header)
        except Exception as e:
            logger.error(f"Error in GetNextPossibleQuestionsService: {e}")
            raise e
