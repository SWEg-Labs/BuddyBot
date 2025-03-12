from models.question import Question
from models.answer import Answer
from models.document import Document
from use_cases.chatUseCase import ChatUseCase
from services.similaritySearchService import SimilaritySearchService
from services.generateAnswerService import GenerateAnswerService
from utils.logger import logger
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
class ChatService(ChatUseCase):
    """
    A service class that processes user input and generates a response using a language model.
    
    Requires instances of SimilaritySearchService and GenerateAnswerService.

    Raises:
        Exception: If an error occurs during initialization.
    """

    def __init__(self, similarity_search_service: SimilaritySearchService, generate_answer_service: GenerateAnswerService):
        """
        Initializes the ChatService with the required services.
        Args:
            similarity_search_service (SimilaritySearchService): An instance of the SimilaritySearchService.
            generate_answer_service (GenerateAnswerService): An instance of the GenerateAnswerService.
        """
        self.__similarity_search_service = similarity_search_service
        self.__generate_answer_service = generate_answer_service

    def get_answer(self, user_input: Question) -> Answer:
        """
        Processes the user input to generate an answer.

        Args:
            user_input (Question): The user's input question.

        Returns:
            Answer: The generated answer.
        """
        try:
            relevant_docs = self.similarity_search(user_input)
            answer = self.generate_answer(user_input, relevant_docs)
            return answer
        except Exception as e:
            logger.error(f"Error in get_answer: {e}")
            raise e

    def similarity_search(self, user_input: Question) -> list[Document]:
        """
        Searches for relevant documents based on user input.

        Args:
            user_input (Question): The user's input question.

        Returns:
            list[Document]: The relevant documents.
        """
        try:
            return self.__similarity_search_service.similarity_search(user_input)
        except Exception as e:
            logger.error(f"Error in similarity_search: {e}")
            raise e

    def generate_answer(self, user_input: Question, relevant_docs: list[Document]) -> Answer:
        """
        Generates an answer based on user input and relevant documents.

        Args:
            user_input (Question): The user's input question.
            relevant_docs (list[Document]): The relevant documents.

        Returns:
            Answer: The generated answer.
        """
        try:
            return self.__generate_answer_service.generate_answer(user_input, relevant_docs)
        except Exception as e:
            logger.error(f"Error in generate_answer: {e}")
            raise e
