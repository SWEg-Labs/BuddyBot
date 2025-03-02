from models.question import Question
from models.answer import Answer
from models.header import Header
from models.document import Document
from entities.langChainDocumentEntity import LangChainDocumentEntity
from repositories.langChainRepository import LangChainRepository

class LangChainAdapter:
    """
    Adapter class for integrating with the LangChainRepository. This class is responsible for
    adapting the input parameters to the format expected by the LangChainRepository and 
    generating answers based on user input and relevant documents.
    """
    def __init__(self, langchain_repository: LangChainRepository):
        """
        Initialize the LangChainAdapter with a LangChainRepository instance.
        Args:
            langchain_repository (LangChainRepository): An instance of LangChainRepository used to generate answers.
        """
        try:
            self.__langchain_repository = langchain_repository
        except Exception as e:
            print(f"An error occurred during initialization: {e}")

    def generate_answer(self, user_input: Question, relevant_docs: list[Document], header: Header) -> Answer:
        """
        Generate an answer based on the user input, relevant documents, and header.
        Args:
            user_input (Question): The user's question.
            relevant_docs (list[Document]): A list of relevant documents to consider for generating the answer.
            header (Header): Additional header information to be used in generating the answer.
        Returns:
            Answer: An Answer object containing the generated answer content.
        Raises:
            Exception: If an error occurs during answer generation
        """

        try:
            # Adapt the parameters to the format expected by LangChainRepository
            user_input = user_input.get_content()
            relevant_docs = [
                LangChainDocumentEntity(page_content=doc.get_page_content(), metadata=doc.get_metadata())
                for doc in relevant_docs
            ]
            header = header.get_content()

            # Call the generate_answer method of LangChainRepository
            generated_answer = self.__langchain_repository.generate_answer(user_input, relevant_docs, header)

            # Create an Answer object with the generated answer content
            answer = Answer(content=generated_answer)

            return answer
        except Exception as e:
            print(f"An error occurred: {e}")

    #def get_next_possible_questions(self, question_answer_couple: QuestionAnswerCouple, header: Header) -> PossibleQuestions:
        # Implement the logic to get the next possible questions based on question_answer_couple and header
    #    pass