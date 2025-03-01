import re
from typing import List

from models.document import Document
from utils.logger import logger

class ConfluenceCleanerService:
    """
    Service class to clean Confluence pages by removing HTML tags and replacing HTML entities.
    """
    def clean_confluence_pages(self, pages: List[Document]) -> List[Document]:
        """
        Cleans the content of a list of Confluence pages by removing HTML tags.
        Args:
            pages (List[Document]): List of Document objects representing Confluence pages.
        Returns:
            List[Document]: List of Document objects with cleaned content.
        Raises:
            Exception: If an error occurs during the cleaning process.
        """
        try:
            for page in pages:
                page.page_content = self._remove_html_tags(page.page_content)
            return pages
        except Exception as e:
            logger.error(f"Error cleaning confluence pages: {e}")
            raise e

    def _remove_html_tags(self, text: str) -> str:
        """
        Removes HTML tags from the given text.
        Args:
            text (str): The text from which HTML tags need to be removed.
        Returns:
            str: The text with HTML tags removed.
        Raises:
            Exception: If an error occurs during the removal of HTML tags.
        """
        try:
            clean = re.sub(r'<[^>]+>', ' ', text)
            return self._replace_html_entities(clean)
        except Exception as e:
            logger.error(f"Error removing HTML tags: {e}")
            raise e

    def _replace_html_entities(self, text: str) -> str:
        """
        Replaces HTML entities in the given text with their corresponding characters.
        Args:
            text (str): The text in which HTML entities need to be replaced.
        Returns:
            str: The text with HTML entities replaced by their corresponding characters.
        Raises:
            Exception: If an error occurs during the replacement of HTML entities.
        """
        try:
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
        except Exception as e:
            logger.error(f"Error replacing HTML entities: {e}")
            raise e
