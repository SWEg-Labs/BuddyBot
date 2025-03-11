from models.question import Question
from models.answer import Answer
from models.header import Header
from models.document import Document
from ports.generateAnswerPort import GenerateAnswerPort
from utils.logger import logger
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
class GenerateAnswerService:
    """
    Service class responsible for generating answers based on user input and relevant documents.
    Attributes:
        header (Header): The header information required for generating answers.
        generate_answer_port (GenerateAnswerPort): The port used to generate answers.
    """

    def __init__(self, header: Header, generate_answer_port: GenerateAnswerPort):
        """
        Initializes the GenerateAnswerService with the given header and generate_answer_port.
        Args:
            header (Header): The header information required for generating answers.
            generate_answer_port (GenerateAnswerPort): The port used to generate answers.
        """
        self.__header = header
        self.__generate_answer_port = generate_answer_port

    def generate_answer(self, user_input: Question, relevant_docs: list[Document]) -> Answer:
        """
        Generates an answer based on the user input and relevant documents.
        Args:
            user_input (Question): The user's question input.
            relevant_docs (list[Document]): A list of relevant documents to consider for generating the answer.
        Returns:
            Answer: The generated answer.
        """
        try:
            answer = self.__generate_answer_port.generate_answer(user_input, relevant_docs, self.__header)
            return answer
        except Exception as e:
           logger.error(f"An error occurred while generating the answer: {e}")
           raise e
