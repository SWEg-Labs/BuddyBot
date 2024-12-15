from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from repositories.vectorStoreRepository import VectorStoreRepository
from utils.logger import logger

class ChatService:
    def __init__(self, llm: ChatOpenAI, vector_store: VectorStoreRepository):
        try:
            self.llm = llm
            self.vector_store = vector_store
        except Exception as e:
            logger.error(f"Error initializing ChatService: {e}")

    def process_user_input(self, user_input: str) -> str:
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
