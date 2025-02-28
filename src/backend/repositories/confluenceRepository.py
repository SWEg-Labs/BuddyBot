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
            self.base_url = base_url
            self.project_key = project_key
            self.timeout = timeout
            self.headers = headers
        except Exception as e:
            logger.error(f"Error initializing ConfluenceRepository: {e}")
            raise

    def load_confluence_pages(self) -> Tuple[PlatformLog, List[PageEntity]]:
        """
        Fetches pages from the Confluence space.
        Returns:
            Tuple[PlatformLog, List[PageEntity]]: A tuple containing a log of the operation and a list of pages.
        Raises:
            requests.RequestException: If there is an error during the API request.
        """
        try:
            url = f"{self.base_url}/rest/api/content"
            params = {
                "spaceKey": self.project_key,
                "expand": "body.view,version,ancestors,space,extensions,links",
                "limit": 50
            }

            response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
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

            log = PlatformLog(LoadingItems.ConfluencePages, datetime.now(), True)

            return log, pages
        except requests.RequestException as e:
            logger.error(f"Error fetching Confluence pages: {e}")
            log = PlatformLog(LoadingItems.ConfluencePages, datetime.now(), False)
            return log, []
