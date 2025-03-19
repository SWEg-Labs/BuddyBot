from beartype.typing import List, Tuple
from datetime import datetime
import pytz
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

            github_files_with_new_metadata = self.get_github_files_new_metadata(github_files, github_commits)
            cleaned_confluence_pages = self.clean_confluence_pages(confluence_pages)

            documents = github_commits + github_files_with_new_metadata + jira_issues + cleaned_confluence_pages
            vector_store_log = self.load_in_vector_store(documents)

            platform_logs = [github_commits_log, github_files_log, jira_issues_log, confluence_pages_log]
            loading_attempt = LoadingAttempt(platform_logs, vector_store_log, starting_timestamp)

            db_save_operation_response = self.save_loading_attempt_in_db(loading_attempt)
            if db_save_operation_response.get_success():
                logger.info("Loading attempt successfully saved in Postgres database.")
            else:
                raise Exception("Failed to save loading attempt in Postgres database: Connection to the database failed. "
                                "Details: " + db_save_operation_response.get_message())

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

    def get_github_files_new_metadata(self, github_files: List[Document], github_commits: List[Document]) -> List[Document]:
        """
        Aggiorna i metadati dei GitHub File impostando:
        1) "last_update": data dell'ultimo commit (indipendentemente dallo status) in cui il file compare.
        2) "creation_date": data dell'ultimo commit in cui il file compare con status "added" oppure "renamed".
        
        Per ogni file in github_files, viene scansionata la lista dei commit (github_commits). 
        In ciascun commit viene iterata la lista di stringhe presente nel campo "files". 
        Utilizziamo una espressione regolare per estrarre:
        - Il filename, cioè il testo compreso tra "- " e " (Status: "
        - Lo status, cioè il testo compreso tra " (Status: " e ", Changes: "

        Args:
            github_files (List[Document]): La lista di file caricati da GitHub.
            github_commits (List[Document]): La lista di commit caricati da GitHub.

        Returns:
            List[Document]: La lista di file con i metadati aggiornati.

        Raises:
            ValueError: Se il percorso del file non è presente nei metadati del file
                        o se il formato della data nei commit di GitHub non è valido.
        """
        try:
            # L'espressione regolare per estrarre il percorso del file e lo status:
            # - Cattura il filename: tutto ciò che si trova tra "- " e " (Status: "
            # - Cattura lo status: tutto ciò che si trova tra " (Status: " e ", Changes: "
            file_info_pattern = re.compile(r'-\s+(.*?)\s+\(Status:\s+([^,]+),')

            # Itera su ogni file caricato da GitHub
            for gh_file in github_files:
                file_path = gh_file.get_metadata().get("path", "").strip()
                if not file_path:
                    raise ValueError("File path not found in GitHub file metadata.")

                last_update_date = None
                creation_date_date = None

                # Scorri tutti i commit per cercare quelli che riguardano questo file
                for commit in github_commits:
                    commit_date_str = commit.get_metadata().get("date", "")
                    try:
                        commit_date = datetime.strptime(commit_date_str, '%Y-%m-%d %H:%M:%S')
                    except Exception as e:
                        raise ValueError(f"Invalid date format in GitHub commit: {commit_date_str}") from e

                    # Il campo "files" del commit è una lista di stringhe
                    commit_files_list = commit.get_metadata().get("files", [])
                    for file_str in commit_files_list:
                        # Estrae filename e status utilizzando la regex
                        match = file_info_pattern.search(file_str)
                        if match:
                            commit_file_path = match.group(1).strip()
                            status = match.group(2).strip().lower()
                            # Se il filename del commit corrisponde al path del file corrente
                            if commit_file_path == file_path:
                                # Aggiorna "last_update" se il commit è più recente
                                if (last_update_date is None) or (commit_date > last_update_date):
                                    last_update_date = commit_date
                                # Se lo status è "added" o "renamed", aggiorna "creation_date"
                                if status in ["added", "renamed"]:
                                    if (creation_date_date is None) or (commit_date > creation_date_date):
                                        creation_date_date = commit_date

                # Crea un dizionario temporaneo per i metadati aggiornati
                updated_metadata = gh_file.get_metadata().copy()

                # Aggiorna i metadati del file se sono state trovate date valide
                if last_update_date is not None:
                    updated_metadata["last_update"] = last_update_date.strftime('%Y-%m-%d %H:%M:%S')
                if creation_date_date is not None:
                    updated_metadata["creation_date"] = creation_date_date.strftime('%Y-%m-%d %H:%M:%S')

                # Imposta i metadati aggiornati utilizzando il setter
                gh_file.set_metadata(updated_metadata)

            return github_files
        except Exception as e:
            logger.error(f"Error in get_github_files_new_metadata: {e}")
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
                f"Tentativo di aggiornamento del database vettoriale:\n"
                f"- Esito: {'riuscito' if loading_attempt.get_outcome() else 'fallito'}\n"
                f"- Elementi interessati: {', '.join([log.get_loading_items().value for log in loading_attempt.get_platform_logs()])}\n"
                f"- Data e ora di inizio: {loading_attempt.get_starting_timestamp().strftime('%Y/%m/%d %H:%M:%S')}\n"
                f"- Data e ora di fine: {loading_attempt.get_ending_timestamp().strftime('%Y/%m/%d %H:%M:%S')}\n"
                f"- Numero elementi aggiunti: {loading_attempt.get_vector_store_log().get_num_added_items()}\n"
                f"- Numero elementi modificati: {loading_attempt.get_vector_store_log().get_num_modified_items()}\n"
                f"- Numero elementi eliminati: {loading_attempt.get_vector_store_log().get_num_deleted_items()}\n"
                "=============================================\n"
            )
            file_logger.info(log_message)

            logger.info("Loading attempt successfully saved in TXT file.")
        except Exception as e:
            logger.error(f"Error saving loading attempt in TXT file: {e}")
            raise e
