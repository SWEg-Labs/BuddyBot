from controllers.userController import UserController
from repositories.vectorStoreRepository import VectorStoreRepository
from services.githubService import GithubService
from services.jiraService import JiraService
from services.confluenceService import ConfluenceService

def update_database():
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
        UserController._load_github_files(*args)
        UserController._load_github_commits(*args)
        UserController._load_jira(*args)
        UserController._load_confluence(*args)
    except Exception as e:
        raise e

if __name__ == "__main__":
    update_database()
