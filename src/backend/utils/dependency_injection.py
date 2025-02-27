import os
from dotenv import load_dotenv
import chromadb

from models.header import Header
from models.documentConstraints import DocumentConstraints
from repositories.chromaVectorStoreRepository import ChromaVectorStoreRepository
from adapters.chromaVectorStoreAdapter import ChromaVectorStoreAdapter
from services.similaritySearchService import SimilaritySearchService
from repositories.langChainRepository import LangChainRepository
from adapters.langChainAdapter import LangChainAdapter
from services.generateAnswerService import GenerateAnswerService
from services.chatService import ChatService
from controllers.chatController import ChatController
# from services.githubService import GithubService
# from services.jiraService import JiraService
# from services.confluenceService import ConfluenceService
from utils.inizialize_llm import initialize_llm


def dependency_injection():
    """
    Configura e restituisce le dipendenze necessarie per l'applicazione BuddyBot.

    Carica le variabili d'ambiente, inizializza i servizi e i controller necessari per il funzionamento del bot.
    """
    try:
        # Caricamento delle variabili d'ambiente
        load_dotenv()

        # Tipi di supporto
        document_constraints = DocumentConstraints(1.2, 0.3)
        llm = initialize_llm()
        generate_answer_header = Header("""Sei un assistente virtuale esperto che risponde a domande in italiano.
                    Di seguito di verrà fornita una domanda dall'utente e un contesto, e riguarderanno 
                    codice, issues o documentazione di un'azienda informatica, provenienti rispettivamente da GitHub, Jira e Confluence.
                    Rispondi alla domanda basandoti esclusivamente sui dati forniti come contesto,
                    dando una spiegazione dettagliata ed esaustiva della risposta data.
                    Se possibile rispondi con un elenco puntato o numerato.
                    Se la domanda ti chiede informazioni allora tu cercale nel contesto e forniscile.
                    Se non riesci a trovare la risposta nei documenti forniti, ma la domanda è comunque legata all'informatica,
                    rispondi con "Informazione non trovata".
                    Se l'utente è uscito dal contesto informatico, rispondi con "La domanda è fuori contesto".
                    """)

        # Chroma
        chroma_client = chromadb.HttpClient(host=os.getenv("CHROMA_HOST", "localhost"),
                                            port=int(os.getenv("CHROMA_PORT", "8000"))) # Connessione al server ChromaDB
        chroma_client.heartbeat()  # Verifica connessione
        chroma_collection_name = "buddybot-vector-store"
        chroma_collection = chroma_client.get_or_create_collection(name=chroma_collection_name) # Crea o ottieni una collezione esistente

        # Catena di similarity search
        chroma_vector_store_repository = ChromaVectorStoreRepository(chroma_client, chroma_collection_name, chroma_collection)
        max_chunk_size = 41666  # 42 KB
        vector_store_adapter = ChromaVectorStoreAdapter(max_chunk_size, chroma_vector_store_repository)
        similarity_search_service = SimilaritySearchService(document_constraints, vector_store_adapter)

        # Catena di generate answer
        langchain_repository = LangChainRepository(llm)
        langchain_adapter = LangChainAdapter(langchain_repository)
        generate_answer_service = GenerateAnswerService(generate_answer_header, langchain_adapter)

        # Catena di chat
        chat_service = ChatService(similarity_search_service, generate_answer_service)
        chat_controller = ChatController(chat_service)

        # Piattaforme per l'accesso ai dati
        # github_service = GithubService()
        # jira_service = JiraService()
        # confluence_service = ConfluenceService()

        return {
            "chat_controller": chat_controller,
            # Altri controller
        }
    except Exception as e:
        print(f"Errore durante l'inizializzazione delle dipendenze: {e}")
        return None