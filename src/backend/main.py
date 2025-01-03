import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

from services.githubService import GithubService
from services.jiraService import JiraService
from services.confluenceService import ConfluenceService
from repositories.vectorStoreRepository import VectorStoreRepository
from utils.llm import initialize_llm
from services.chatService import ChatService
from utils.logger import logger
from controllers.userController import UserController

def main():
    """
    Main function to run the chat application.

    Initializes the language model, vector store, chat service, and other services.
    Provides a command-line interface for interacting with the chat application.

    Raises:
        Exception: If an error occurs during initialization or processing.
    """
    try:
        # inizialize language model
        llm = initialize_llm()

        # inizialize vector store
        vector_store = VectorStoreRepository()

        # create chat service instance
        chat_service = ChatService(llm, vector_store)

        # create the github service instance
        github_service = GithubService()

        # create the jira service instance
        jira_service = JiraService()

        # create the confluence service instance
        confluence_service = ConfluenceService()

        logger.info('Chat initialized. You can:\n' \
                    '- Type a Message\n' \
                    '- Write "exit" to quit\n' \
                    '- Write "help" to see the available commands\n' \
                    '- Write "lgf" to load files from GitHub into the Chroma database \n' \
                    '- Write "lgc" to load commits from GitHub into the Chroma database \n' \
                    '- Write "lj" to load issues from Jira into the Chroma database \n' \
                    '- Write "lc" to load pages from Confluence into the Chroma database \n' \
                    '- Write "dr" to delete and recreate the Chroma collection \n' \
                    '- Write "v" to view all Chroma documents')

        UserController.ask_question(vector_store, chat_service, github_service, jira_service, confluence_service)
    except Exception as e:
        logger.error(f"Failed to start the chat: {e}")

if __name__ == "__main__":
    main()
