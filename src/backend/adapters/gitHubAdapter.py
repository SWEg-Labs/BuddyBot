import base64
from typing import List, Tuple

from models.document import Document
from models.loggingModels import PlatformLog
from ports.gitHubPort import GitHubPort
from repositories.gitHubRepository import GitHubRepository
from utils.logger import logger

class GitHubAdapter(GitHubPort):
    """
    Adapter class for interacting with a GitHub repository.
    This class provides methods to load commits and files from a GitHub repository
    and convert them into a document format.
    """

    def __init__(self, github_repository: GitHubRepository):
        """
        Initialize the GitHubAdapter with a GitHubRepository instance.
        Args:
            github_repository (GitHubRepository): An instance of GitHubRepository to interact with GitHub.
        Raises:
            Exception: If there is an error during initialization.
        """
        try:
            self.__github_repository = github_repository
        except Exception as e:
            logger.error(f"Error initializing GitHubAdapter: {e}")
            raise

    def load_github_commits(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Load commits from the GitHub repository and convert them into documents.
        Returns:
            tuple: A tuple containing the log and a list of Document instances representing the commits.
        Raises:
            Exception: If there is an error while loading commits.
        """
        try:
            log, commit_entities = self.__github_repository.load_github_commits()
            documents = [
                Document(
                    page_content=commit.get_message()
                    if commit.get_message() is not None
                    else "/",
                    metadata={
                        "author": commit.get_author_name()
                        if commit.get_author_name() is not None
                        else "/",
                        "email": commit.get_author_email()
                        if commit.get_author_email() is not None
                        else "/",
                        "date": commit.get_author_date()
                        if commit.get_author_date() is not None
                        else "/",
                        "files": [
                            (
                                f"- {file.get_filename() if file.get_filename() is not None else '/'} "
                                f"(Status: {file.get_status() if file.get_status() is not None else '/'}, "
                                f"Changes: {file.get_changes() if file.get_changes() is not None else '/'}, "
                                f"Additions: {file.get_additions() if file.get_additions() is not None else '/'}, "
                                f"Deletions: {file.get_deletions() if file.get_deletions() is not None else '/'})\n"
                                f"  Patch:\n{file.get_patch() if file.get_patch() is not None else '/'}"
                            )
                            for file in (commit.get_files() if commit.get_files() is not None else [])
                        ],
                        "url": commit.get_url()
                        if commit.get_url() is not None
                        else "/",
                        "id": commit.get_sha() if commit.get_sha() is not None else "/",
                    },
                )
                for commit in (commit_entities if commit_entities is not None else [])
            ]
            return log, documents
        except Exception as e:
            logger.error(f"Error while adapting GitHub commits: {e}")
            raise

    def load_github_files(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Load files from the GitHub repository and convert them into documents.
        Returns:
            tuple: A tuple containing the log and a list of Document instances representing the files.
        Raises:
            Exception: If there is an error while loading files.
        """
        try:
            log, file_entities = self.__github_repository.load_github_files()
            documents = []
            for file in file_entities:
                try:
                    documents.append(
                        Document(
                            page_content=base64.b64decode(file.get_content()).decode('utf-8')
                            if file.get_content() is not None
                            else "/",
                            metadata={
                                "type": file.get_type() if file.get_type() is not None else "/",
                                "name": file.get_name() if file.get_name() is not None else "/",
                                "path": file.get_path() if file.get_path() is not None else "/",
                                "url": file.get_html_url() if file.get_html_url() is not None else "/",
                                "id": file.get_sha() if file.get_sha() is not None else "/",
                            },
                        )
                    )
                except UnicodeDecodeError as e:
                    logger.info(f"Skipping file {file.get_path()} due to decoding error: {e}")
            return log, documents
        except Exception as e:
            logger.error(f"Error while adapting GitHub files: {e}")
            raise
