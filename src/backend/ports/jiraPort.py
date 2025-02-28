from abc import ABC, abstractmethod
from typing import Tuple, List

from models.document import Document
from models.loggingModels import PlatformLog

class JiraPort(ABC):
    """
    Interface for Jira operations.
    This interface defines methods to load Jira issues and adapt them into documents.
    """

    @abstractmethod
    def load_jira_issues(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Loads Jira issues and adapts them into a list of Document objects.
        Returns:
            Tuple[PlatformLog, List[Document]]: A tuple containing the platform log and a list of adapted documents.
        Raises:
            Exception: If an error occurs while loading or adapting Jira issues.
        """
        pass
