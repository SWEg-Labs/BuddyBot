import logging
import structlog
from typing import List, Tuple
import re

from models.document import Document
from models.loggingModels import PlatformLog, VectorStoreLog, LoadingAttempt
from models.dbSaveOperationResponse import DbSaveOperationResponse
from use_cases.loadFilesUseCase import LoadFilesUseCase
from ports.gitHubPort import GitHubPort
from ports.jiraPort import JiraPort
from ports.confluencePort import ConfluencePort
from ports.loadFilesInVectorStorePort import LoadFilesInVectorStorePort
from ports.saveLoadingAttemptInDbPort import SaveLoadingAttemptInDbPort
from services.confluenceCleanerService import ConfluenceCleanerService

class LoadFilesService(LoadFilesUseCase):
    """
    Service class responsible for loading files from various platforms (GitHub, Jira, Confluence),
    cleaning Confluence pages, and saving the loading attempt logs.
    Attributes:
        github_port (GitHubPort): Port for interacting with GitHub.
        jira_port (JiraPort): Port for interacting with Jira.
        confluence_port (ConfluencePort): Port for interacting with Confluence.
        load_files_in_vector_store_port (LoadFilesInVectorStorePort): Port for loading files into a vector store.
        save_loading_attempt_in_db_port (SaveLoadingAttemptInDbPort): Port for saving loading attempts in the database.
        confluence_cleaner_service (ConfluenceCleanerService): Service for cleaning Confluence pages.
    """

    def __init__(self, github_port: GitHubPort, jira_port: JiraPort, confluence_port: ConfluencePort, confluence_cleaner_service: ConfluenceCleanerService, 
                 load_files_in_vector_store_port: LoadFilesInVectorStorePort, save_loading_attempt_in_db_port: SaveLoadingAttemptInDbPort):
        """
        Initializes the LoadFilesService with the given ports and services.
        Args:
            github_port (GitHubPort): Port for interacting with GitHub.
            jira_port (JiraPort): Port for interacting with Jira.
            confluence_port (ConfluencePort): Port for interacting with Confluence.
            load_files_in_vector_store_port (LoadFilesInVectorStorePort): Port for loading files into a vector store.
            save_loading_attempt_in_db_port (SaveLoadingAttemptInDbPort): Port for saving loading attempts in the database.
            confluence_cleaner_service (ConfluenceCleanerService): Service for cleaning Confluence pages.
        """
        try:
            self.github_port = github_port
            self.jira_port = jira_port
            self.confluence_port = confluence_port
            self.confluence_cleaner_service = confluence_cleaner_service
            self.load_files_in_vector_store_port = load_files_in_vector_store_port
            self.save_loading_attempt_in_db_port = save_loading_attempt_in_db_port
        except Exception as e:
            logging.error(f"Error initializing LoadFilesService: {e}")
            raise

    def load(self):
        """
        Loads data from GitHub, Jira, and Confluence, cleans Confluence pages, and saves the loading attempt logs.
        """
        try:
            github_commits_log, github_commits = self.load_github_commits()
            github_files_log, github_files = self.load_github_files()
            jira_issues_log, jira_issues = self.load_jira_issues()
            confluence_pages_log, confluence_pages = self.load_confluence_pages()
            
            cleaned_confluence_pages = self.clean_confluence_pages(confluence_pages)
            
            documents = github_commits + github_files + jira_issues + cleaned_confluence_pages
            vector_store_log = self.load_in_vector_store(documents)
            
            platform_logs = [github_commits_log, github_files_log, jira_issues_log, confluence_pages_log]
            loading_attempt = LoadingAttempt(platform_logs, vector_store_log)
            
            self.save_loading_attempt_in_db(loading_attempt)
            self.save_loading_attempt_in_txt(loading_attempt)
        except Exception as e:
            logging.error(f"Error in load method: {e}")
            raise

    def load_github_commits(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Loads GitHub commits.
        Returns:
            Tuple[PlatformLog, List[Document]]: A tuple containing the platform log and a list of documents.
        """
        try:
            return self.github_port.load_github_commits()
        except Exception as e:
            logging.error(f"Error loading GitHub commits: {e}")
            raise

    def load_github_files(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Loads GitHub files.
        Returns:
            Tuple[PlatformLog, List[Document]]: A tuple containing the platform log and a list of documents.
        """
        try:
            return self.github_port.load_github_files()
        except Exception as e:
            logging.error(f"Error loading GitHub files: {e}")
            raise

    def load_jira_issues(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Loads Jira issues.
        Returns:
            Tuple[PlatformLog, List[Document]]: A tuple containing the platform log and a list of documents.
        """
        try:
            return self.jira_port.load_jira_issues()
        except Exception as e:
            logging.error(f"Error loading Jira issues: {e}")
            raise

    def load_confluence_pages(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Loads Confluence pages.
        Returns:
            Tuple[PlatformLog, List[Document]]: A tuple containing the platform log and a list of documents.
        """
        try:
            return self.confluence_port.load_confluence_pages()
        except Exception as e:
            logging.error(f"Error loading Confluence pages: {e}")
            raise

    def clean_confluence_pages(self, pages: List[Document]) -> List[Document]:
        """
        Cleans Confluence pages.
        Args:
            pages (List[Document]): A list of Confluence pages to be cleaned.
        Returns:
            List[Document]: A list of cleaned Confluence pages.
        """
        try:
            return self.confluence_cleaner_service.clean_confluence_pages(pages)
        except Exception as e:
            logging.error(f"Error cleaning Confluence pages: {e}")
            raise

    def load_in_vector_store(self, documents: List[Document]) -> VectorStoreLog:
        """
        Loads documents into a vector store.
        Args:
            documents (List[Document]): A list of documents to be loaded into the vector store.
        Returns:
            VectorStoreLog: The log of the vector store loading operation.
        """
        try:
            return self.load_files_in_vector_store_port.load(documents)
        except Exception as e:
            logging.error(f"Error loading documents in vector store: {e}")
            raise

    def save_loading_attempt_in_db(self, loading_attempt: LoadingAttempt) -> DbSaveOperationResponse:
        """
        Saves the loading attempt in the database.
        Args:
            loading_attempt (LoadingAttempt): The loading attempt to be saved.
        Returns:
            DbSaveOperationResponse: The response of the database save operation.
        """
        try:
            return self.save_loading_attempt_in_db_port.save_loading_attempt(loading_attempt)
        except Exception as e:
            logging.error(f"Error saving loading attempt in DB: {e}")
            raise

    def save_loading_attempt_in_txt(self, loading_attempt: LoadingAttempt):
        """
        Saves the loading attempt in a TXT file.
        Args:
            loading_attempt (LoadingAttempt): The loading attempt to be saved.
        """
        try:
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(message)s",
                handlers=[
                    logging.FileHandler("../../../../log_aggiornamento_automatico.txt", mode='a'),
                    logging.StreamHandler()
                ]
            )
            structlog.configure(
                processors=[
                    structlog.processors.TimeStamper(fmt="iso"),
                    structlog.processors.JSONRenderer()
                ],
                logger_factory=structlog.stdlib.LoggerFactory()
            )
            logger = structlog.get_logger()
            log_message = (
                "=============================================\n"
                f"Tentativo aggiornamento database vettoriale:\n"
                f"- Esito: {'riuscito' if loading_attempt.outcome else 'fallito'}\n"
                f"- Elementi interessati: {', '.join([log.loading_items.value for log in loading_attempt.platform_logs])}\n"
                f"- Data di inizio: {loading_attempt.starting_timestamp.strftime('%Y/%m/%d %H:%M:%S')}\n"
                f"- Data di fine: {loading_attempt.ending_timestamp.strftime('%Y/%m/%d %H:%M:%S')}\n"
                f"- Numero elementi aggiunti: {loading_attempt.vector_store_log.num_added_items}\n"
                f"- Numero elementi modificati: {loading_attempt.vector_store_log.num_modified_items}\n"
                f"- Numero elementi eliminati: {loading_attempt.vector_store_log.num_deleted_items}\n"
            )
            logger.info(log_message)
        except Exception as e:
            logging.error(f"Error saving loading attempt in TXT: {e}")
            raise
