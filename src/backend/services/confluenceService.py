import os
import requests
import base64
import re
from utils.logger import logger
from langchain.schema import Document

class ConfluenceService:
    """
    A class that provides methods for interacting with the Confluence API.

    Requires
    - `ATLASSIAN_TOKEN` and `ATLASSIAN_USER_EMAIL` environment variables for authentication.
    - `CONFLUENCE_BASE_URL` and `CONFLUENCE_SPACE_KEY` environment variables for configuration.

    Raises:
        ValueError: If any of the required environment variables are missing.
    """
    def __init__(self):
        """
        Initializes the Confluence client using the required environment variables.

        Raises:
            Exception: If an error occurs during initialization.
        """
        try:
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
        except Exception as e:
            logger.error(f"Error initializing Confluence client: {e}")
            raise

    def _replace_html_entities(self, text):
        replacements = {
            '&agrave;': 'à',
            '&egrave;': 'è',
            '&igrave;': 'ì',
            '&ograve;': 'ò',
            '&ugrave;': 'ù',
            '&quot;': '"',
            '&Egrave;' : 'È',
        }
        for entity, char in replacements.items():
            text = text.replace(entity, char)
        return text

    def _remove_html_tags(self, text):
        clean = re.sub(r'<[^>]+>', ' ', text)
        return self._replace_html_entities(clean)
    
    def _clean_content(self, pages):
        for page in pages:
            html_content = page.get('body', {}).get('storage', {}).get('value', '')
            if html_content:
                page['body']['storage']['value'] = self._remove_html_tags(html_content)
        return pages

    def get_pages(self):
        """
        Fetches a list of pages from the Confluence space.

        Returns:
            list: A list of Confluence page objects.

        Raises:
            Exception: If an error occurs while fetching pages.
        """
        try:
            url = f"{self.base_url}/rest/api/content"
            params = {
                "spaceKey": self.space_key,
                "expand": "body.storage,version",
                "limit": 50
            }
            response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            response.raise_for_status()

            pages = response.json().get("results", [])

            print(f"Found {len(pages)} pages")
            print(pages)

            cleaned_pages = self._clean_content(pages)

            print(f"Cleaned {len(cleaned_pages)} pages")
            print(cleaned_pages)

            return pages
        except Exception as e:
            logger.error(f"Error fetching pages: {e}")
            raise

    def get_page_details(self, page_id):
        """
        Fetches the details of a specific Confluence page.

        Args:
            page_id (str): The ID of the Confluence page.

        Returns:
            dict: A dictionary containing the details of the Confluence page.

        Raises:
            Exception: If an error occurs while fetching page details.
        """
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

    def get_space_overview(self):
        """
        Fetches the overview of the Confluence space.

        Returns:
            dict: A dictionary containing the overview of the Confluence space.

        Raises:
            Exception: If an error occurs while fetching the space overview.
        """
        try:
            url = f"{self.base_url}/rest/api/space/{self.space_key}"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching space overview: {e}")
            raise
