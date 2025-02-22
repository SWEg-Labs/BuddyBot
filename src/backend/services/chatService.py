from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from repositories.similaritySearchService import SimilaritySearchService
from usecases.chatUseCase import ChatUseCase
from utils.logger import logger

class ChatService(ChatUseCase):
    """
    A service class that processes user input and generates a response using a language model.
    
    Requires an instance of the ChatOpenAI language model and a ChromaVectorStoreRepository instance

    Raises:
        Exception: If an error occurs during initialization.
    """
    def __init__(self, llm: ChatOpenAI, similarity_search_service: SimilaritySearchService):
        """
        Initializes the ChatService with a language model and a vector store repository.

        Args:
            llm (ChatOpenAI): An instance of the ChatOpenAI language model.
            similarity_search_service (ChromaVectorStoreRepository): An instance of the ChromaVectorStoreRepository.

        Raises:
            Exception: If an error occurs during initialization.
        """
        try:
            self.llm = llm
            self.similarity_search_service = similarity_search_service
            self.header = """Sei un assistente virtuale esperto che risponde a domande in italiano.
                            Di seguito di verrà fornita una domanda dall'utente e un contesto, e riguarderanno 
                            codice, issues o documentazione di un'azienda informatica, provenienti rispettivamente da GitHub, Jira e Confluence.
                            Rispondi alla domanda basandoti esclusivamente sui dati forniti come contesto,
                            dando una spiegazione dettagliata ed esaustiva della risposta data.
                            Se possibile rispondi con un elenco puntato o numerato.
                            Se la domanda ti chiede informazioni allora tu cercale nel contesto e forniscile.
                            Se non riesci a trovare la risposta nei documenti forniti, ma la domanda è comunque legata all'informatica,
                            rispondi con "Informazione non trovata".
                            Se l'utente è uscito dal contesto informatico, rispondi con "La domanda è fuori contesto".
                            """
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
            relevant_docs = self.similarity_search_service.similarity_search(user_input)
            logger.info(f"Found {len(relevant_docs)} relevant documents")

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
                "header": self.header,
                "user_input": user_input,
                "context": relevant_docs
            })

            return response
        except Exception as e:
            logger.error(f"Error processing user input: {e}")
            raise
