from abc import ABC, abstractmethod
from beartype.typing import Tuple, List

from models.document import Document
from models.loggingModels import PlatformLog

class ConfluencePort(ABC):
    """
    Interface for Confluence operations.
    This interface defines methods to load Confluence pages and adapt them into documents.
    """

    @abstractmethod
    def load_confluence_pages(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Loads Confluence pages and converts them to Document objects.
        Returns:
            Tuple[PlatformLog, List[Document]]: A tuple containing the platform log and a list of Document objects.
        Raises:
            Exception: If there is an error loading the Confluence pages.
        """
        pass