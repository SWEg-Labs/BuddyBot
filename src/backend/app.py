from typing import Dict
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

from business_data_classes.header import Header
from repositories.chromaVectorStoreRepository import ChromaVectorStoreRepository
from adapters.chromaVectorStoreAdapter import ChromaVectorStoreAdapter
from services.similaritySearchService import SimilaritySearchService
from repositories.langChainRepository import LangChainRepository
from adapters.langChainAdapter import LangChainAdapter
from services.generateAnswerService import GenerateAnswerService
from services.chatService import ChatService
from controllers.chatController import ChatController
from services.githubService import GithubService
from services.jiraService import JiraService
from services.confluenceService import ConfluenceService
from controllers.userController import UserController
from utils.inizialize_llm import initialize_llm
from utils.logger import logger

# Inizializzazione dell'app FastAPI
app = FastAPI(
    title="BuddyBot API",
    description="Un'API per interagire con un chatbot che utilizza dati da GitHub, Jira e "\
    "Confluence.",
    version="1.0.0"
)

# Configurazione CORS per permettere richieste dal client Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caricamento delle variabili d'ambiente
load_dotenv()

# Tipi di supporto
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
# generate_possible_questions_header =

# Catena di similarity search
chroma_vector_store_repository = ChromaVectorStoreRepository()
vector_store_adapter = ChromaVectorStoreAdapter(chroma_vector_store_repository)
similarity_search_service = SimilaritySearchService(vector_store_adapter)

# Catena di generate answer
langchain_repository = LangChainRepository(llm)
langchain_adapter = LangChainAdapter(langchain_repository)
generate_answer_service = GenerateAnswerService(generate_answer_header, langchain_adapter)

# Catena di chat
chat_service = ChatService(similarity_search_service, generate_answer_service)
chat_controller = ChatController(chat_service)

# Piattaforme per l'accesso ai dati
github_service = GithubService()
jira_service = JiraService()
confluence_service = ConfluenceService()


@app.post("/api/chat", summary="Invia un messaggio al chatbot", response_model=Dict[str, str])
async def chat(request: Request):
    """
    Endpoint per inviare un messaggio al chatbot e ottenere una risposta.

    Args:
        request (Request): La richiesta JSON contenente il messaggio dell'utente.

    Returns:
        Dict[str, str]: Una risposta JSON con la risposta del chatbot.
    
    Body JSON esempio:
        {
            "message": "Ciao, chatbot!"
        }
    """
    return await chat_controller.get_answer(request)


@app.get("/api/github/load", summary="Carica i file da GitHub", response_model=Dict[str, str])
async def load_from_github():
    """
    Endpoint per caricare i file da GitHub nel database Chroma.

    Returns:
        Dict[str, str]: Stato dell'operazione con un messaggio.
    """
    try:
        UserController.load_github_files(chroma_vector_store_repository, github_service)
        UserController.load_github_commits(chroma_vector_store_repository, github_service)
        return {"response": "File caricati con successo da GitHub"}
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)


@app.get("/api/jira/load", summary="Carica le issue da Jira", response_model=Dict[str, str])
async def load_from_jira():
    """
    Endpoint per caricare le issue da Jira nel database Chroma.

    Returns:
        Dict[str, str]: Stato dell'operazione con un messaggio.
    """
    try:
        UserController.load_jira(chroma_vector_store_repository, github_service, jira_service)
        return {"response": "File caricati con successo da Jira"}
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)


@app.get("/api/confluence/load", summary="Carica le pagine da Confluence",
         response_model=Dict[str, str])
async def load_from_confluence():
    """
    Endpoint per caricare le pagine da Confluence nel database Chroma.

    Returns:
        Dict[str, str]: Stato dell'operazione con un messaggio.
    """
    try:
        UserController.load_confluence(chroma_vector_store_repository, github_service, jira_service,
                                       confluence_service)
        return {"response": "File caricati con successo da Confluence"}
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
