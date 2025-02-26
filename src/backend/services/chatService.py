from langchain.chains.combine_documents import create_stuff_documents_chain
from models.question import Question
from models.answer import Answer
from models.document import Document
from services.similaritySearchService import SimilaritySearchService
from services.generateAnswerService import GenerateAnswerService
from use_cases.chatUseCase import ChatUseCase
from utils.logger import logger

class ChatService(ChatUseCase):
    """
    A service class that processes user input and generates a response using a language model.
    
    Requires an instance of the ChatOpenAI language model and a ChromaVectorStoreRepository instance

    Raises:
        Exception: If an error occurs during initialization.
    """
    def __init__(self, similarity_search_service: SimilaritySearchService, generate_answer_service: GenerateAnswerService):
        """
        Initializes the ChatService with a language model and a vector store repository.

        Args:
            similarity_search_service (ChromaVectorStoreRepository): An instance of the ChromaVectorStoreRepository.
            generate_answer_service (GenerateAnswerService): An instance of the GenerateAnswerService.

        Raises:
            Exception: If an error occurs during initialization.
        """
        try:
            self.similarity_search_service = similarity_search_service
            self.generate_answer_service = generate_answer_service
        except Exception as e:
            logger.error(f"Error initializing ChatService: {e}")

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
            return None

    def similarity_search(self, user_input: Question) -> list[Document]:
        """
        Searches for relevant documents based on user input.

        Args:
            user_input (Question): The user's input question.

        Returns:
            list[Document]: The relevant documents.
        """
        try:
            return self.similarity_search_service.similarity_search(user_input)
        except Exception as e:
            logger.error(f"Error in similarity_search: {e}")
            return None

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
            return self.generate_answer_service.generate(user_input, relevant_docs)
        except Exception as e:
            logger.error(f"Error in generate_answer: {e}")
            return None