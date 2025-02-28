from typing import List, Tuple

from models.document import Document
from models.loggingModels import PlatformLog
from ports.confluencePort import ConfluencePort
from repositories.confluenceRepository import ConfluenceRepository
from utils.logger import logger

class ConfluenceAdapter(ConfluencePort):
    """
    Adapter class for interacting with Confluence through a repository.
    Attributes:
        confluence_repository (ConfluenceRepository): The repository used to interact with Confluence.
    """

    def __init__(self, confluence_repository: ConfluenceRepository):
        """
        Initializes the ConfluenceAdapter with the given repository.
        Args:
            confluence_repository (ConfluenceRepository): The repository used to interact with Confluence.
        Raises:
            Exception: If there is an error initializing the adapter.
        """
        try:
            self.confluence_repository = confluence_repository
        except Exception as e:
            logger.error(f"Error initializing ConfluenceAdapter: {e}")
            raise

    def load_confluence_pages(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Loads Confluence pages and converts them to Document objects.
        Returns:
            Tuple[PlatformLog, List[Document]]: A tuple containing the platform log and a list of Document objects.
        Raises:
            Exception: If there is an error loading the Confluence pages.
        """
        try:
            platform_log, page_entities = self.confluence_repository.load_confluence_pages()
            documents = [
                Document(
                    page_content=page.body["storage"]["value"],
                    metadata={
                        "title": page.title,
                        "space": page.space["name"],
                        "created_by": page.version["by"]["displayName"],
                        "created_date": page.version["when"],
                        "url": f"{self.confluence_repository.base_url}{page.links['webui']}",
                        "id": page.id,
                    }
                )
            for page in page_entities]
            return platform_log, documents
        except Exception as e:
            logger.error(f"Error adapting Confluence pages: {e}")
            return None, []
