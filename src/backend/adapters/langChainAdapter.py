from models.question import Question
from models.answer import Answer
from models.header import Header
from models.document import Document
from models.questionAnswerCouple import QuestionAnswerCouple
from models.nextPossibleQuestions import NextPossibleQuestions
from models.possibleQuestion import PossibleQuestion
from entities.langChainDocumentEntity import LangChainDocumentEntity
from ports.generateAnswerPort import GenerateAnswerPort
from ports.getNextPossibleQuestionsPort import GetNextPossibleQuestionsPort
from repositories.langChainRepository import LangChainRepository
from utils.logger import logger

class LangChainAdapter(GenerateAnswerPort, GetNextPossibleQuestionsPort):
    """
    Adapter class for integrating with the LangChainRepository. This class is responsible for
    adapting the input parameters to the format expected by the LangChainRepository and 
    generating answers based on user input and relevant documents.
    """
    def __init__(self, max_num_tokens: int, langchain_repository: LangChainRepository):
        """
        Initialize the LangChainAdapter with a LangChainRepository instance.
        Args:
            max_num_tokens (int): The maximum number of tokens allowed for the LLM.
            langchain_repository (LangChainRepository): An instance of LangChainRepository used to generate answers.
        """
        try:
            self.__max_num_tokens = max_num_tokens
            self.__langchain_repository = langchain_repository
        except Exception as e:
            logger.error(f"An error occurred during initialization: {e}")
            raise e

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
            header = header.get_content()

            # Aggiorna page_content di ogni documento con metadati e contenuto completo
            # Perchè create_stuff_documents_chain fornisce al chatbot solo il campo page_content di ogni documento
            for doc in relevant_docs:
                doc.set_page_content(f"Metadata: {doc.get_metadata()}\nContent: {doc.get_page_content()}")

            # Inizializza il conteggio dei token con header e user_input (in quest'ordine)
            total_tokens = self.__count_tokens(header) + self.__count_tokens(user_input)
            filtered_docs = []

            # Aggiungi i documenti uno ad uno finché il limite non viene superato.
            for doc in relevant_docs:
                doc_tokens = self.__count_tokens(doc.get_page_content())
                if total_tokens + doc_tokens >= self.__max_num_tokens:
                    break
                filtered_docs.append(doc)
                total_tokens += doc_tokens

            relevant_docs = filtered_docs

            # Converti i documenti in un formato accettato da LangChainRepository
            relevant_docs = [
                LangChainDocumentEntity(page_content=doc.get_page_content(), metadata=doc.get_metadata())
                for doc in relevant_docs
            ]

            # Call the generate_answer method of LangChainRepository
            generated_answer = self.__langchain_repository.generate_answer(user_input, relevant_docs, header)

            # Create an Answer object with the generated answer content
            answer = Answer(content=generated_answer)

            return answer
        except Exception as e:
            logger.error(f"An error occured in generate_answer of LangChainAdapter: {e}")
            raise e

    def get_next_possible_questions(self, question_answer_couple: QuestionAnswerCouple, header: Header) -> NextPossibleQuestions:
        """
        Retrieves the next possible questions based on the provided question-answer couple and header.
        Args:
            question_answer_couple (QuestionAnswerCouple): The question-answer couple.
            header (Header): The header information.
        Returns:
            NextPossibleQuestions: The next possible questions.
        Raises:
            Exception: If there is an error during the retrieval process.
        """
        try:
            # Extract content from question and answer
            question_content = question_answer_couple.get_question().get_content()
            answer_content = question_answer_couple.get_answer().get_content()

            # Call the repository method to get the next possible questions
            repo_response = self.__langchain_repository.get_next_possible_questions(
                [question_content, answer_content],
                header.get_content()
            )

            # Parse the repository response to create NextPossibleQuestions object
            questions = repo_response.split("___")
            questions = [q.strip() for q in questions if q.strip()]

            possible_questions = [PossibleQuestion(q) for q in questions]
            next_possible_questions = NextPossibleQuestions(num_questions=len(possible_questions), possible_questions=possible_questions)

            return next_possible_questions
        except Exception as e:
            logger.error(f"An error occured in get_next_possible_questions of LangChainAdapter: {e}")
            raise e

    def __count_tokens(self, text: str) -> int:
        """
        Calculates the approximate number of tokens based on the provided text.
        Approximation: roughly 1 token every 3 characters.
        Args:
            text (str): The text for which to calculate the number of tokens.
        Returns:
            int: The approximate number of tokens.
        Raises:
            Exception: If an error occurs during token calculation.
        """
        try:
            return max(1, int(len(text) / 3))
        except Exception as e:
            logger.error(f"An error occurred during token calculation: {e}")
            raise e
