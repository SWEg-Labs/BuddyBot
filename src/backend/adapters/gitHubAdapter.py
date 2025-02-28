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
            self.github_repository = github_repository
        except Exception as e:
            logger.error(f"Error initializing GitHubAdapter: {e}")

    def load_github_commits(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Load commits from the GitHub repository and convert them into documents.
        Returns:
            tuple: A tuple containing the log and a list of Document instances representing the commits.
        Raises:
            Exception: If there is an error while loading commits.
        """
        try:
            log, commit_entities = self.github_repository.load_github_commits()
            documents = [
                Document(
                    page_content=commit.message,
                    metadata={
                        "author": commit.author_name,
                        "email": commit.author_email,
                        "date": commit.author_date,
                        "files": [
                            f"- {file.filename} (Status: {file.status}, Changes: {file.changes}, Additions: {file.additions}, Deletions: {file.deletions})\n  Patch:\n{file.patch}"
                            for file in commit.files
                        ],
                        "url": commit.url,
                        "id": commit.sha,
                    }
                )
                for commit in commit_entities
            ]
            return log, documents
        except Exception as e:
            logger.error(f"Error while adapting GitHub commits: {e}")

    def load_github_files(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Load files from the GitHub repository and convert them into documents.
        Returns:
            tuple: A tuple containing the log and a list of Document instances representing the files.
        Raises:
            Exception: If there is an error while loading files.
        """
        try:
            log, file_entities = self.github_repository.load_github_files()
            documents = [
                Document(
                    page_content=base64.b64decode(file.content).decode('utf-8'),
                    metadata={
                        "type": file.type,
                        "name": file.name,
                        "path": file.path,
                        "url": file.html_url,
                        "id": file.sha,
                    }
                )
                for file in file_entities
            ]
            return log, documents
        except Exception as e:
            logger.error(f"Error while adapting GitHub files: {e}")
            return None, []
