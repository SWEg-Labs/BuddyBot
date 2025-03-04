import requests
from datetime import datetime
from typing import List, Tuple

from models.loggingModels import PlatformLog, LoadingItems
from entities.pageEntity import PageEntity
from utils.logger import logger

class ConfluenceRepository:
    """
    Repository class to interact with Confluence API.
    Attributes:
        base_url (str): The base URL of the Confluence instance.
        project_key (str): The key of the Confluence project/space.
        timeout (int): The timeout for API requests.
        headers (dict[str, str]): The headers to include in API requests.
    """

    def __init__(self, base_url: str, project_key: str, timeout: int, headers: dict[str, str]):
        """
        Initializes the ConfluenceRepository with the given parameters.

        Args:
            base_url (str): The base URL of the Confluence instance.
            project_key (str): The key of the Confluence project/space.
            timeout (int): The timeout for API requests.
            headers (dict[str, str]): The headers to include in API requests.
        """
        try:
            self.__base_url = base_url
            self.__project_key = project_key
            self.__timeout = timeout
            self.__headers = headers
        except Exception as e:
            logger.error(f"Error initializing ConfluenceRepository: {e}")
            raise

    def get_base_url(self) -> str:
        """
        Returns the base URL of the Confluence instance.
        Returns:
            str: The base URL of the Confluence instance.
        """
        return self.__base_url

    def load_confluence_pages(self) -> Tuple[PlatformLog, List[PageEntity]]:
        """
        Fetches pages from the Confluence space.
        Returns:
            Tuple[PlatformLog, List[PageEntity]]: A tuple containing a log of the operation and a list of pages.
        Raises:
            requests.RequestException: If there is an error during the API request.
        """
        try:
            url = f"{self.__base_url}/rest/api/content"
            params = {
                "spaceKey": self.__project_key,
                "expand": "body.view,version,ancestors,space,extensions,links",
                "limit": 50
            }

            response = requests.get(url, headers=self.__headers, params=params, timeout=self.__timeout)
            response.raise_for_status()
            pages_data = response.json().get('results', [])

            pages = [PageEntity(
                id=page['id'],
                type=page['type'],
                title=page['title'],
                space=page['space'],
                body=page['body'],
                version=page['version'],
                status=page['status'],
                ancestors=page['ancestors'],
                extensions=page['extensions'],
                links=page['_links']
            ) for page in pages_data]

            logger.info(f"Fetched {len(pages)} pages from Confluence space {self.__project_key}")
            log = PlatformLog(LoadingItems.ConfluencePages, datetime.now(), True)

            return log, pages
        except requests.RequestException as e:
            logger.error(f"Error fetching Confluence pages: {e}")
            log = PlatformLog(LoadingItems.ConfluencePages, datetime.now(), False)
            raise
