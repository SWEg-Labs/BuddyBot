from abc import ABC, abstractmethod
from beartype.typing import Tuple, List

from models.document import Document
from models.loggingModels import PlatformLog

class GitHubPort(ABC):
    """
    Interface for GitHub operations.
    This interface defines methods to load commits and files from a GitHub repository and adapt them into documents.
    """
    
    @abstractmethod
    def load_github_commits(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Load commits from the GitHub repository and convert them into documents.
        Returns:
            tuple: A tuple containing the log and a list of Document instances representing the commits.
        """
        pass

    @abstractmethod
    def load_github_files(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Load files from the GitHub repository and convert them into documents.
        Returns:
            tuple: A tuple containing the log and a list of Document instances representing the files.
        Raises:
            Exception: If there is an error while loading files.
        """
        pass
