from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

from entities.langChainDocumentEntity import LangChainDocumentEntity
from utils.logger import logger
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
class LangChainRepository:
    """
    A repository class that processes user input and generates a response using a language model.
    Requires an instance of the ChatOpenAI language model.
    Raises:
        Exception: If an error occurs during initialization.
    """

    def __init__(self, llm: ChatOpenAI):
        """
        Initializes the LangChainRepository with a language model.
        Args:
            llm (ChatOpenAI): An instance of the ChatOpenAI language model.
        """
        self.__llm = llm

    def generate_answer(self, user_input: str, relevant_docs: list[LangChainDocumentEntity], header: str) -> str:
        """
        Generates an answer based on the user's input and relevant documents.
        Args:
            user_input (str): The input provided by the user.
            relevant_docs (list[LangChainDocumentEntity]): A list of relevant documents to provide context.
            header (str): A header to include in the prompt.
        Returns:
            str: The generated response from the language model.
        Raises:
            Exception: If an error occurs while processing the user input.
        """
        try:
            # Crea un PromptTemplate per il modello AI
            prompt = ChatPromptTemplate.from_messages(
                [("user", "{header}\n\n\n{user_input}\n\n\n{context}")]
            )

            # Crea una catena RAG (Retrieval-Augmented Generation)
            rag_chain = create_stuff_documents_chain(
                llm=self.__llm,
                prompt=prompt
            )

            print("relevant_docs : ")
            for i, doc in enumerate(relevant_docs, start=1):
                print(f"\nDocumento {i}:\n{doc.get_page_content()}")
            print("\n\n\n\n")

            # Esegue la catena per ottenere una risposta
            response = rag_chain.invoke({
                "header": header,
                "user_input": user_input,
                "context": relevant_docs
            })

            logger.info(f"Generated response: {response}")

            return response
        except Exception as e:
            logger.error(f"Error getting the answer in LangChainRepository: {e}")
            raise e

    def get_next_possible_questions(self, question_answer_couple: list[LangChainDocumentEntity], header: str) -> str:
        """
        Generates the next possible questions based on a given question-answer pair and a header.
        Args:
            question_answer_couple (list[LangChainDocumentEntity]): A list containing a question and its corresponding answer.
            header (str): A header string to provide context for the AI model.
        Returns:
            str: A string containing the possible next questions generated by the AI model.
        Raises:
            Exception: If there is an error during the generation process, it logs the error and raises an exception.
        """
        try:
            # Crea un PromptTemplate per il modello AI
            prompt = ChatPromptTemplate.from_messages(
                [("user", "{header}\n\n\n{context}")]
            )

            # Crea una catena RAG (Retrieval-Augmented Generation)
            rag_chain = create_stuff_documents_chain(
                llm=self.__llm,
                prompt=prompt
            )

            # Esegue la catena per ottenere le prossime domande possibili
            response = rag_chain.invoke({
                "header": header,
                "context": question_answer_couple
            })

            logger.info(f"Generated next possible questions: {response}")

            return response
        except Exception as e:
            logger.error(f"Error getting next possible questions in LangChainRepository: {e}")
            raise e
