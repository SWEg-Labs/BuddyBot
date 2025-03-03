import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import chromadb
from github import Github
import base64
import psycopg2

from models.header import Header
from models.documentConstraints import DocumentConstraints
from controllers.chatController import ChatController
from controllers.loadFilesController import LoadFilesController
from controllers.saveMessageController import SaveMessageController
from controllers.getMessagesController import GetMessagesController
from services.similaritySearchService import SimilaritySearchService
from services.generateAnswerService import GenerateAnswerService
from services.chatService import ChatService
from services.confluenceCleanerService import ConfluenceCleanerService
from services.loadFilesService import LoadFilesService
from services.saveMessageService import SaveMessageService
from services.getMessagesService import GetMessagesService
from adapters.chromaVectorStoreAdapter import ChromaVectorStoreAdapter
from adapters.langChainAdapter import LangChainAdapter
from adapters.gitHubAdapter import GitHubAdapter
from adapters.jiraAdapter import JiraAdapter
from adapters.confluenceAdapter import ConfluenceAdapter
from adapters.postgresAdapter import PostgresAdapter
from repositories.chromaVectorStoreRepository import ChromaVectorStoreRepository
from repositories.langChainRepository import LangChainRepository
from repositories.gitHubRepository import GitHubRepository
from repositories.jiraRepository import JiraRepository
from repositories.confluenceRepository import ConfluenceRepository
from repositories.postgresRepository import PostgresRepository
from utils.logger import logger


def initialize_langchain() -> LangChainAdapter:
    """
    Initializes and returns an instance of LangChainAdapter.
    Initializes the LLM model using the credentials and model name specified in the environment variables.
    Returns:
      - LangChainAdapter: An instance of LangChainAdapter.
    Raises:
      - Exception: If an error occurs during LangChain initialization.
    """
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")  # Default model name
        llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model_name=model_name,
        )
        langchain_repository = LangChainRepository(llm)
        langchain_adapter = LangChainAdapter(langchain_repository)
        logger.info(f"LLM model loaded: {model_name}")
        return langchain_adapter
    except Exception as e:
        logger.error(f"Error during LangChain initialization: {e}")
        raise e

def initialize_chroma() -> ChromaVectorStoreAdapter:
    """
    Initializes and returns an instance of ChromaVectorStoreAdapter.
    Configures the ChromaDB client and creates or retrieves an existing collection.
    Returns:
      - ChromaVectorStoreAdapter: An instance of ChromaVectorStoreAdapter.
    Raises:
      - Exception: If an error occurs during Chroma initialization.
    """
    try:
        chroma_client = chromadb.HttpClient(host=os.getenv("CHROMA_HOST", "localhost"),
                                            port=int(os.getenv("CHROMA_PORT", "8000")))  # Connessione al server ChromaDB
        chroma_client.heartbeat()  # Verifica connessione
        chroma_collection_name = "buddybot-vector-store"
        chroma_collection = chroma_client.get_or_create_collection(name=chroma_collection_name)  # Crea o ottieni una collezione esistente
        chroma_vector_store_repository = ChromaVectorStoreRepository(chroma_client, chroma_collection_name, chroma_collection)
        max_chunk_size = 41666  # 42 KB
        chroma_vector_store_adapter = ChromaVectorStoreAdapter(max_chunk_size, chroma_vector_store_repository)
        logger.info("ChromaDB collection loaded")
        return chroma_vector_store_adapter
    except Exception as e:
        logger.error(f"Error during Chroma initialization: {e}")
        raise e

def initialize_postgres() -> PostgresAdapter:
    """
    Initializes and returns an instance of PostgresAdapter.
    Configures the connection to the Postgres database using the credentials specified in the environment variables.
    Returns:
      - PostgresAdapter: An instance of PostgresAdapter.
    Raises:
      - Exception: If an error occurs during Postgres initialization.
    """
    try:
        DB_CONFIG = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432"),
            "user": os.getenv("DB_USER", "buddybot"),
            "password": os.getenv("DB_PASSWORD", "buddybot"),
            "dbname": os.getenv("DB_NAME", "buddybot")
        }
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            dbname=DB_CONFIG["dbname"]
        )
        postgres_repository = PostgresRepository(conn)
        postgres_adapter = PostgresAdapter(postgres_repository)
        logger.info("Postgres database loaded")
        return postgres_adapter
    except Exception as e:
        logger.error(f"Error during Postgres initialization: {e}")
        raise e

def initialize_github() -> GitHubAdapter:
    """
    Initializes and returns an instance of GitHubAdapter.
    Configures the GitHub client using the token specified in the environment variables and retrieves the specified repository.
    Returns:
      - GitHubAdapter: An instance of GitHubAdapter.
    Raises:
      - Exception: If an error occurs during GitHub initialization.
    """
    try:
        github_token = os.getenv("GITHUB_TOKEN")
        github = Github(github_token)
        github_repo = github.get_repo(f"{os.getenv('OWNER')}/{os.getenv('REPO')}")
        github_repository = GitHubRepository(github_repo)
        github_adapter = GitHubAdapter(github_repository)
        logger.info("GitHub repository loaded")
        return github_adapter
    except Exception as e:
        logger.error(f"Error during GitHub initialization: {e}")
        raise e

def initialize_atlassian() -> tuple[int, dict[str, str]]:
    """
    Initializes and returns the configuration parameters for Atlassian.
    Configures the authentication and timeout parameters for Atlassian requests.
    Returns:
      - tuple[int, dict[str, str]]: Request timeout and authentication headers.
    Raises:
      - Exception: If an error occurs during Atlassian initialization.
    """
    try:
        atlassian_token = os.getenv("ATLASSIAN_TOKEN")
        atlassian_user_email = os.getenv("ATLASSIAN_USER_EMAIL")
        requests_timeout = int(os.getenv("TIMEOUT", "10"))
        requests_auth_str = f"{atlassian_user_email}:{atlassian_token}"
        requests_auth_bytes = base64.b64encode(requests_auth_str.encode("utf-8")).decode("utf-8")
        requests_headers = {
            "Authorization": f"Basic {requests_auth_bytes}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        return requests_timeout, requests_headers
    except Exception as e:
        logger.error(f"Error during Atlassian initialization: {e}")
        raise e

def initialize_jira(requests_timeout: int, requests_headers: dict[str, str]) -> JiraAdapter:
    """
    Initializes and returns an instance of JiraAdapter.
    Configures the Jira client using the specified configuration parameters.
    Args:
      - requests_timeout (int): Request timeout.
      - requests_headers (dict[str, str]): Authentication headers.
    Returns:
      - JiraAdapter: An instance of JiraAdapter.
    Raises:
      - Exception: If an error occurs during Jira initialization.
    """
    try:
        jira_base_url = os.getenv("JIRA_BASE_URL")
        jira_project_key = os.getenv("JIRA_PROJECT_KEY")
        jira_repository = JiraRepository(jira_base_url, jira_project_key, requests_timeout, requests_headers)
        jira_adapter = JiraAdapter(jira_repository)
        logger.info("Jira project loaded")
        return jira_adapter
    except Exception as e:
        logger.error(f"Error during Jira initialization: {e}")
        raise e

def initialize_confluence(requests_timeout: int, requests_headers: dict[str, str]) -> ConfluenceAdapter:
    """
    Initializes and returns an instance of ConfluenceAdapter.
    Configures the Confluence client using the specified configuration parameters.
    Args:
      - requests_timeout (int): Request timeout.
      - requests_headers (dict[str, str]): Authentication headers.
    Returns:
      - ConfluenceAdapter: An instance of ConfluenceAdapter.
    Raises:
      - Exception: If an error occurs during Confluence initialization.
    """
    try:
        confluence_base_url = os.getenv("CONFLUENCE_BASE_URL")
        confluence_space_key = os.getenv("CONFLUENCE_SPACE_KEY")
        confluence_repository = ConfluenceRepository(confluence_base_url, confluence_space_key, requests_timeout, requests_headers)
        confluence_adapter = ConfluenceAdapter(confluence_repository)
        logger.info("Confluence space loaded")
        return confluence_adapter
    except Exception as e:
        logger.error(f"Error during Confluence initialization: {e}")
        raise e




def dependency_injection_frontend() -> dict[str, object]:
    """
    Configures and returns the dependencies needed for the BuddyBot application frontend.
    Returns:
      - dict[str, object]: A dictionary containing the configured dependencies.
    Raises:
      - Exception: If an error occurs during frontend dependencies initialization.
    """
    try:
        # Caricamento delle variabili d'ambiente
        load_dotenv()



        # ======================== 1. Architettura della generazione di una risposta ========================

        # Tipi di supporto
        document_constraints = DocumentConstraints(1.2, 0.3)
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
        
        # LangChain
        langchain_adapter = initialize_langchain()

        # Chroma
        chroma_vector_store_adapter = initialize_chroma()

        # Catena di chat
        similarity_search_service = SimilaritySearchService(document_constraints, chroma_vector_store_adapter)
        generate_answer_service = GenerateAnswerService(generate_answer_header, langchain_adapter)
        chat_service = ChatService(similarity_search_service, generate_answer_service)
        chat_controller = ChatController(chat_service)



        # ========= 6. Architettura backend dell'aggiornamento del badge di segnalazione esito aggiornamento automatico ==========

        # ...



        # =========================== 7. Architettura del salvataggio dei messaggi nello storico ============================

        # Postgres
        postgres_adapter = initialize_postgres()
        
        # Catena di save_message
        save_message_service = SaveMessageService(postgres_adapter)
        save_message_controller = SaveMessageController(save_message_service)



        # ============================= 8. Architettura del recupero dei messaggi dallo storico =============================

        # Catena di get_messages
        get_messages_service = GetMessagesService(postgres_adapter)
        get_messages_controller = GetMessagesController(get_messages_service)



        # ==================== 9. Architettura della generazione di domande per proseguire la conversazione ====================

        # ...



        return {
            "chat_controller": chat_controller,
            # "get_last_load_outcome_controller": get_last_load_outcome_controller,
            "save_message_controller": save_message_controller,
            "get_messages_controller": get_messages_controller,
            # "get_next_possible_questions_controller": get_next_possible_questions_controller
        }
    except Exception as e:
        logger.error(f"Error during frontend dependencies initialization: {e}")
        raise e




def dependency_injection_cron() -> dict[str, object]:
    """
    Configures and returns the dependencies needed for the cron functionality.
    Returns:
      - dict[str, object]: A dictionary containing the configured dependencies.
    Raises:
      - Exception: If an error occurs during cron dependencies initialization.
    """
    try:
        # Caricamento delle variabili d'ambiente
        load_dotenv()



        # ======================== 2. Architettura dell'aggiornamento automatico del database vettoriale ========================

        # GitHub
        github_adapter = initialize_github()

        # Atlassian (Jira e Confluence)
        requests_timeout, requests_headers = initialize_atlassian()

        # Jira
        jira_adapter = initialize_jira(requests_timeout, requests_headers)

        # Confluence
        confluence_adapter = initialize_confluence(requests_timeout, requests_headers)
        confluence_cleaner_service = ConfluenceCleanerService()

        # Chroma
        chroma_vector_store_adapter = initialize_chroma()

        # Postgres
        postgres_adapter = initialize_postgres()

        # Catena di load_files
        load_files_service = LoadFilesService(github_adapter, jira_adapter, confluence_adapter, confluence_cleaner_service,
                                              chroma_vector_store_adapter, postgres_adapter)
        load_files_controller = LoadFilesController(load_files_service)



        return {
            "load_files_controller": load_files_controller
        }
    except Exception as e:
        logger.error(f"Error during cron dependencies initialization: {e}")
        raise e
