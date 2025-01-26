from controllers.userController import UserController
from repositories.vectorStoreRepository import VectorStoreRepository
from services.githubService import GithubService
from services.jiraService import JiraService
from services.confluenceService import ConfluenceService
from utils.logger import logger

def update_database():
    """
    Funzione per aggiornare il database con i dati da GitHub, Jira e Confluence.

    Raises:
        Exception: Se si verifica un errore durante l'aggiornamento del database.
    """
    print("Chiamata funzione update_database")
    try:
        # inizializza vector store
        vector_store = VectorStoreRepository()
        # inizializza github service
        github_service = GithubService()
        # inizializza jira service
        jira_service = JiraService()
        # inizializza confluence service
        confluence_service = ConfluenceService()
        # set args vector
        args = (vector_store, github_service, jira_service, confluence_service)

        # update database
        UserController.load_github_files(*args)
        UserController.load_github_commits(*args)
        UserController.load_jira(*args)
        UserController.load_confluence(*args)
    except Exception as e:
        logger.error(f"Failed to update the database: {e}")
        raise e

if __name__ == "__main__":
    update_database()
