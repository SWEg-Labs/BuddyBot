import os
from dotenv import load_dotenv
import chromadb
from github import Github
import base64
import psycopg2

from models.header import Header
from models.documentConstraints import DocumentConstraints
from controllers.chatController import ChatController
from services.similaritySearchService import SimilaritySearchService
from services.generateAnswerService import GenerateAnswerService
from services.chatService import ChatService
from adapters.chromaVectorStoreAdapter import ChromaVectorStoreAdapter
from adapters.langChainAdapter import LangChainAdapter
from adapters.gitHubAdapter import GitHubAdapter
from adapters.jiraAdapter import JiraAdapter
from repositories.chromaVectorStoreRepository import ChromaVectorStoreRepository
from repositories.langChainRepository import LangChainRepository
from repositories.gitHubRepository import GitHubRepository
from repositories.jiraRepository import JiraRepository
from utils.inizialize_llm import initialize_llm
from utils.logger import Logger


def dependency_injection():
    """
    Configura e restituisce le dipendenze necessarie per l'applicazione BuddyBot.

    Carica le variabili d'ambiente, inizializza i servizi e i controller necessari per il funzionamento del bot.
    """
    try:
        # Caricamento delle variabili d'ambiente
        load_dotenv()


        # ======================== 1. Architettura della generazione di una risposta ========================

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
        chroma_vector_store_adapter = ChromaVectorStoreAdapter(max_chunk_size, chroma_vector_store_repository)
        similarity_search_service = SimilaritySearchService(document_constraints, chroma_vector_store_adapter)

        # Catena di generate answer
        langchain_repository = LangChainRepository(llm)
        langchain_adapter = LangChainAdapter(langchain_repository)
        generate_answer_service = GenerateAnswerService(generate_answer_header, langchain_adapter)

        # Catena di chat
        chat_service = ChatService(similarity_search_service, generate_answer_service)
        chat_controller = ChatController(chat_service)


        # ======================== 2. Architettura dell'aggiornamento automatico del database vettoriale ========================

        # GitHub
        github_token = os.getenv("GITHUB_TOKEN")
        github = Github(github_token)
        github_repo = github.get_repo(f"{os.getenv("OWNER")}/{os.getenv("REPO")}")
        github_repository = GitHubRepository(github_repo)
        github_adapter = GitHubAdapter(github_repository)

        # Atlassian (Jira e Confluence)
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

        # Jira
        jira_base_url = os.getenv("JIRA_BASE_URL")
        jira_project_key = os.getenv("JIRA_PROJECT_KEY")
        jira_repository = JiraRepository(jira_base_url, jira_project_key, requests_timeout, requests_headers)
        jira_adapter = JiraAdapter(jira_repository)

        # Confluence
        confluence_base_url = os.getenv("CONFLUENCE_BASE_URL")
        confluence_space_key = os.getenv("CONFLUENCE_SPACE_KEY")
        confluence_repository = JiraRepository(confluence_base_url, confluence_space_key, requests_timeout, requests_headers)
        confluence_adapter = JiraAdapter(confluence_repository)

        # Postgres
        DB_CONFIG = {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "dbname": os.getenv("DB_NAME")
        }
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            dbname=DB_CONFIG["dbname"]
        )
        postgres_repository = PostgresRepository(conn)




        return {
            "chat_controller": chat_controller,
            # Altri controller
        }
    except Exception as e:
        Logger.error(f"Errore durante l'inizializzazione delle dipendenze: {e}")
        return None