from beartype.typing import List, Tuple
from datetime import datetime
import pytz

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
from utils.logger import logger, file_logger
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
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
        self.__github_port = github_port
        self.__jira_port = jira_port
        self.__confluence_port = confluence_port
        self.__confluence_cleaner_service = confluence_cleaner_service
        self.__load_files_in_vector_store_port = load_files_in_vector_store_port
        self.__save_loading_attempt_in_db_port = save_loading_attempt_in_db_port

    def load(self):
        """
        Loads data from GitHub, Jira, and Confluence, cleans Confluence pages, and saves the loading attempt logs.
        """
        try:
            italy_tz = pytz.timezone('Europe/Rome')
            starting_timestamp = datetime.now(italy_tz)

            github_commits_log, github_commits = self.load_github_commits()
            github_files_log, github_files = self.load_github_files()
            jira_issues_log, jira_issues = self.load_jira_issues()
            confluence_pages_log, confluence_pages = self.load_confluence_pages()

            cleaned_confluence_pages = self.clean_confluence_pages(confluence_pages)

            documents = github_commits + github_files + jira_issues + cleaned_confluence_pages
            vector_store_log = self.load_in_vector_store(documents)

            platform_logs = [github_commits_log, github_files_log, jira_issues_log, confluence_pages_log]
            loading_attempt = LoadingAttempt(platform_logs, vector_store_log, starting_timestamp)

            db_save_operation_response = self.save_loading_attempt_in_db(loading_attempt)
            if not db_save_operation_response.get_success():
                raise Exception("Failed to save loading attempt in Postgres database: Connection to the database failed. "
                                "Details: " + db_save_operation_response.get_message())
            else:
                logger.info("Loading attempt correctly saved in Postgres database.")

            self.save_loading_attempt_in_txt(loading_attempt)
        except Exception as e:
            logger.error(f"Error in load method of LoadFilesService: {e}")
            raise e

    def load_github_commits(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Loads GitHub commits.
        Returns:
            Tuple[PlatformLog, List[Document]]: A tuple containing the platform log and a list of documents.
        """
        try:
            return self.__github_port.load_github_commits()
        except Exception as e:
            logger.error(f"Error loading GitHub commits: {e}")
            raise e

    def load_github_files(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Loads GitHub files.
        Returns:
            Tuple[PlatformLog, List[Document]]: A tuple containing the platform log and a list of documents.
        """
        try:
            return self.__github_port.load_github_files()
        except Exception as e:
            logger.error(f"Error loading GitHub files: {e}")
            raise e

    def load_jira_issues(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Loads Jira issues.
        Returns:
            Tuple[PlatformLog, List[Document]]: A tuple containing the platform log and a list of documents.
        """
        try:
            return self.__jira_port.load_jira_issues()
        except Exception as e:
            logger.error(f"Error loading Jira issues: {e}")
            raise e

    def load_confluence_pages(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Loads Confluence pages.
        Returns:
            Tuple[PlatformLog, List[Document]]: A tuple containing the platform log and a list of documents.
        """
        try:
            return self.__confluence_port.load_confluence_pages()
        except Exception as e:
            logger.error(f"Error loading Confluence pages: {e}")
            raise e

    def clean_confluence_pages(self, pages: List[Document]) -> List[Document]:
        """
        Cleans Confluence pages.
        Args:
            pages (List[Document]): A list of Confluence pages to be cleaned.
        Returns:
            List[Document]: A list of cleaned Confluence pages.
        """
        try:
            return self.__confluence_cleaner_service.clean_confluence_pages(pages)
        except Exception as e:
            logger.error(f"Error cleaning Confluence pages: {e}")
            raise e

    def load_in_vector_store(self, documents: List[Document]) -> VectorStoreLog:
        """
        Loads documents into a vector store.
        Args:
            documents (List[Document]): A list of documents to be loaded into the vector store.
        Returns:
            VectorStoreLog: The log of the vector store loading operation.
        """
        try:
            return self.__load_files_in_vector_store_port.load(documents)
        except Exception as e:
            logger.error(f"Error loading documents in vector store: {e}")
            raise e

    def save_loading_attempt_in_db(self, loading_attempt: LoadingAttempt) -> DbSaveOperationResponse:
        """
        Saves the loading attempt in the database.
        Args:
            loading_attempt (LoadingAttempt): The loading attempt to be saved.
        Returns:
            DbSaveOperationResponse: The response of the database save operation.
        """
        try:
            return self.__save_loading_attempt_in_db_port.save_loading_attempt(loading_attempt)
        except Exception as e:
            logger.error(f"Error saving loading attempt in DB: {e}")
            raise e

    def save_loading_attempt_in_txt(self, loading_attempt: LoadingAttempt):
        """
        Saves the loading attempt in a TXT file.
        Args:
            loading_attempt (LoadingAttempt): The loading attempt to be saved.
        """
        try:
            log_message = (
                "=============================================\n"
                f"Tentativo aggiornamento database vettoriale:\n"
                f"- Esito: {'riuscito' if loading_attempt.get_outcome() else 'fallito'}\n"
                f"- Elementi interessati: {', '.join([log.get_loading_items().value for log in loading_attempt.get_platform_logs()])}\n"
                f"- Data di inizio: {loading_attempt.get_starting_timestamp().strftime('%Y/%m/%d %H:%M:%S')}\n"
                f"- Data di fine: {loading_attempt.get_ending_timestamp().strftime('%Y/%m/%d %H:%M:%S')}\n"
                f"- Numero elementi aggiunti: {loading_attempt.get_vector_store_log().get_num_added_items()}\n"
                f"- Numero elementi modificati: {loading_attempt.get_vector_store_log().get_num_modified_items()}\n"
                f"- Numero elementi eliminati: {loading_attempt.get_vector_store_log().get_num_deleted_items()}\n"
                "=============================================\n"
            )
            file_logger.info(log_message)

            logger.info("Loading attempt correctly saved in TXT file.")
        except Exception as e:
            logger.error(f"Error saving loading attempt in TXT file: {e}")
            raise e
