from langchain_core import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from entities.langChainDocumentEntity import LangChainDocumentEntity
from utils.logger import logger

class LangChainRepository:
    """
    A service class that processes user input and generates a response using a language model.
    
    Requires an instance of the ChatOpenAI language model and a ChromaVectorStoreRepository instance

    Raises:
        Exception: If an error occurs during initialization.
    """
    def __init__(self, llm: ChatOpenAI):
        """
        Initializes the ChatService with a language model and a vector store repository.

        Args:
            llm (ChatOpenAI): An instance of the ChatOpenAI language model.

        Raises:
            Exception: If an error occurs during initialization.
        """
        try:
            self.llm = llm
        except Exception as e:
            logger.error(f"Error initializing ChatService: {e}")

    def generate_answer(self, user_input: str, relevant_docs: LangChainDocumentEntity, header: str) -> str:
        """
        Processes the user's input by performing a similarity search and generating a response.

        Args:
            user_input (str): The input provided by the user.

        Returns:
            str: The generated response from the language model.

        Raises:
            Exception: If an error occurs while processing the user input.
        """
        try:
            # Aggiorna page_content di ogni documento con metadati e contenuto completo
            # Perchè create_stuff_documents_chain fornisce al chatbot solo il campo page_content di ogni documento
            for doc in relevant_docs:
                doc.page_content = f"Metadata: {doc.metadata}\nContent: {doc.page_content}"

            # Crea un PromptTemplate per il modello AI
            prompt = ChatPromptTemplate.from_messages(
                [("user", "{header}\n\n\n{user_input}\n\n\n{context}")]
            )

            # Crea una catena RAG (Retrieval-Augmented Generation)
            rag_chain = create_stuff_documents_chain(
                llm=self.llm,
                prompt=prompt
            )

            print("relevant_docs : ")
            for i, doc in enumerate(relevant_docs, start=1):
                print(f"\nDocumento {i}:\n{doc.page_content}")

            # Esegue la catena per ottenere una risposta
            response = rag_chain.invoke({
                "header": header,
                "user_input": user_input,
                "context": relevant_docs
            })

            return response
        except Exception as e:
            logger.error(f"Error processing user input: {e}")
            raise

    def get_next_possible_questions(self, question_answer_couple: list[str], header: str) -> list[str]:
        try:
            # Crea un PromptTemplate per il modello AI
            prompt = ChatPromptTemplate.from_messages(
            [("user", "{header}\n\n\n{question}\n{answer}")]
            )

            # Crea una catena RAG (Retrieval-Augmented Generation)
            rag_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=prompt
            )

            # Esegue la catena per ottenere le prossime domande possibili
            response = rag_chain.invoke({
            "header": header,
            "question": question_answer_couple[0],
            "answer": question_answer_couple[1]
            })

            return response
        except Exception as e:
            logger.error(f"Error getting next possible questions: {e}")
            raise