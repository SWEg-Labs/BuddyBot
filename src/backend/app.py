from typing import Dict
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from utils.dependency_injection import dependency_injection_frontend
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

frontend_dependencies = dependency_injection_frontend()
chat_controller = frontend_dependencies["chat_controller"]


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
    try:
        return await chat_controller.get_answer(request)
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)


'''
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
'''


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
