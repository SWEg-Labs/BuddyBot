import os
import requests
import base64
from utils.logger import logger
from langchain.schema import Document

class ConfluenceService:
    def __init__(self):
        self.token = os.getenv("ATLASSIAN_TOKEN")
        self.email = os.getenv("ATLASSIAN_USER_EMAIL")
        self.base_url = os.getenv("CONFLUENCE_BASE_URL")
        self.space_key = os.getenv("CONFLUENCE_SPACE_KEY")
        self.timeout = int(os.getenv("TIMEOUT", "10"))

        if not all([self.token, self.email, self.base_url, self.space_key]):
            raise ValueError("Environment variables ATLASSIAN_TOKEN, ATLASSIAN_USER_EMAIL, CONFLUENCE_BASE_URL, or CONFLUENCE_SPACE_KEY are missing.")

        # Codifica in Base64 per l'autenticazione
        auth_str = f"{self.email}:{self.token}"
        auth_bytes = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

        self.headers = {
            "Authorization": f"Basic {auth_bytes}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        logger.info("Initialized Confluence client")

    def get_pages(self):
        """Ottiene le pagine dello spazio Confluence."""
        try:
            url = f"{self.base_url}/rest/api/content"
            params = {
                "spaceKey": self.space_key,
                "expand": "body.storage,version",
                "limit": 50
            }
            response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            response.raise_for_status()

            print(response.json())

            pages = response.json().get("results", [])

            print(f'\n\n\n\n\n\n\n\n\n\n\n\n{pages}')

            return pages
        except Exception as e:
            logger.error(f"Error fetching pages: {e}")
            raise

    def get_page_details(self, page_id):
        """Ottiene i dettagli di una specifica pagina Confluence."""
        try:
            url = f"{self.base_url}/rest/api/content/{page_id}"
            params = {
                "expand": "body.storage,version"
            }
            response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching page details for {page_id}: {e}")
            raise

    def format_data_for_chroma(self, pages):
        """Formatta le pagine di Confluence come Documenti per l'utilizzo con Chroma."""
        documents = []

        for page in pages:
            documents.append(Document(
                page_content=page["body"]["storage"]["value"],
                metadata={
                    "type": "page",
                    "id": page["id"],
                    "title": page["title"],
                    "version": page["version"]["number"],
                    "url": f"{self.base_url}/pages/viewpage.action?pageId={page['id']}"
                }
            ))

        return documents

    def get_space_overview(self):
        """Ottiene un sommario dello spazio Confluence."""
        try:
            url = f"{self.base_url}/rest/api/space/{self.space_key}"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching space overview: {e}")
            raise
