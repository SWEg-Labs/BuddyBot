from beartype.typing import List, Tuple

from models.document import Document
from models.loggingModels import PlatformLog
from ports.confluencePort import ConfluencePort
from repositories.confluenceRepository import ConfluenceRepository
from utils.logger import logger
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
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
            self.__confluence_repository = confluence_repository
        except Exception as e:
            logger.error(f"Error initializing ConfluenceAdapter: {e}")
            raise e

    def load_confluence_pages(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Loads Confluence pages and converts them to Document objects.
        Returns:
            Tuple[PlatformLog, List[Document]]: A tuple containing the platform log and a list of Document objects.
        Raises:
            Exception: If there is an error loading the Confluence pages.
        """
        try:
            platform_log, page_entities = self.__confluence_repository.load_confluence_pages()
            documents = [
                Document(
                    page_content=(
                        page.get_body().get("view").get("value")
                        if page.get_body().get("view").get("value") is not None
                        else "/"
                    ),
                    metadata={
                        "title": (
                            page.get_title()
                            if page.get_title() is not None
                            else "/"
                        ),
                        "space": (
                            page.get_space().get("name")
                            if page.get_space()
                            and page.get_space().get("name") is not None
                            else "/"
                        ),
                        "created_by": (
                            page.get_version().get("by").get("displayName")
                            if page.get_version()
                            and page.get_version().get("by")
                            and page.get_version().get("by").get("displayName") is not None
                            else "/"
                        ),
                        "item_type": "Confluence Page",
                        "creation_date": (
                            page.get_version().get("when")
                            if page.get_version().get("when") is not None
                            else "/"
                        ),
                        "url": (
                            f"{self.__confluence_repository.get_base_url()}{page.get_links().get('webui')}"
                            if page.get_links()
                            and page.get_links().get("webui") is not None
                            else "/"
                        ),
                        "id": (
                            page.get_id()
                            if page.get_id() is not None
                            else "/"
                        ),
                    }
                )
                for page in page_entities
            ]
            return platform_log, documents
        except Exception as e:
            logger.error(f"Error adapting Confluence pages: {e}")
            raise e
