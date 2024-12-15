from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from repositories.vectorStoreRepository import VectorStoreRepository
from utils.logger import logger

class ChatService:
    """
    A service class that processes user input and generates a response using a language model.
    
    Requires an instance of the ChatOpenAI language model and a VectorStoreRepository instance

    Raises:
        Exception: If an error occurs during initialization.
    """
    def __init__(self, llm: ChatOpenAI, vector_store: VectorStoreRepository):
        """
        Initializes the ChatService with a language model and a vector store repository.

        Args:
            llm (ChatOpenAI): An instance of the ChatOpenAI language model.
            vector_store (VectorStoreRepository): An instance of the VectorStoreRepository.

        Raises:
            Exception: If an error occurs during initialization.
        """
        try:
            self.llm = llm
            self.vector_store = vector_store
        except Exception as e:
            logger.error(f"Error initializing ChatService: {e}")

    def process_user_input(self, user_input: str) -> str:
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
            # Esegue una ricerca di similarità per ottenere documenti rilevanti
            relevant_docs = self.vector_store.similarity_search(user_input)
            logger.info(f"Found {len(relevant_docs)} relevant documents")

            # Crea un PromptTemplate per il modello AI
            prompt = ChatPromptTemplate.from_messages(
                [("user", "{user_input}\n\n\n\n{context}")]
            )

            # Crea una catena RAG (Retrieval-Augmented Generation)
            rag_chain = create_stuff_documents_chain(
                llm=self.llm,
                prompt=prompt
            )

            # Esegue la catena per ottenere una risposta
            response = rag_chain.invoke({"user_input": user_input, "context": relevant_docs})

            return response
        except Exception as e:
            logger.error(f"Error processing user input: {e}")
            raise
