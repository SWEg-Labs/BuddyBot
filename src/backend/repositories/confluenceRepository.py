import requests
from datetime import datetime
import pytz
from beartype.typing import List, Tuple

from models.loggingModels import PlatformLog, LoadingItems
from entities.pageEntity import PageEntity
from utils.logger import logger
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
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
        self.__base_url = base_url
        self.__project_key = project_key
        self.__timeout = timeout
        self.__headers = headers

    def get_base_url(self) -> str:
        """
        Returns the base URL of the Confluence instance.
        Returns:
            str: The base URL of the Confluence instance.
        """
        return self.__base_url

    def load_confluence_pages(self) -> Tuple[PlatformLog, List[PageEntity]]:
        """
        Fetches all pages from the Confluence space using pagination.
        Returns:
            Tuple[PlatformLog, List[PageEntity]]: A tuple containing a log of the operation and a list of pages.
        Raises:
            requests.RequestException: If there is an error during the API request.
        """
        try:
            url = f"{self.__base_url}/rest/api/content"
            start = 0
            limit = 100
            pages = []

            while True:
                params = {
                    "spaceKey": self.__project_key,
                    "expand": "body.view,version,ancestors,space,extensions,links",
                    "limit": limit,
                    "start": start
                }

                response = requests.get(url, headers=self.__headers, params=params, timeout=self.__timeout)
                response.raise_for_status()
                data = response.json()
                pages_data = data.get('results', [])
                
                # Converte ogni page in PageEntity
                pages.extend([
                    PageEntity(
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
                    ) for page in pages_data
                ])

                # logger.info(f"Fetched {len(pages_data)} pages (start={start}) from Confluence space {self.__project_key}") # Per debug

                # Incrementa il valore di start per la prossima chiamata
                start += limit

                # Se il numero di elementi restituiti è inferiore al limite, non ci sono altre pagine
                if len(pages_data) < limit:
                    break

            logger.info(f"Fetched {len(pages)} pages from Confluence space {self.__project_key}")
            italy_tz = pytz.timezone('Europe/Rome')
            log = PlatformLog(LoadingItems.ConfluencePages, datetime.now(italy_tz), True)

            return log, pages
        except requests.RequestException as e:
            logger.error(f"Error fetching Confluence pages: {e}")
            italy_tz = pytz.timezone('Europe/Rome')
            log = PlatformLog(LoadingItems.ConfluencePages, datetime.now(italy_tz), False)
            return log, []
        except Exception as e:
            logger.error(f"Error loading Confluence pages: {e}")
            raise e
