import re
from beartype.typing import List

from models.document import Document
from utils.logger import logger
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
class ConfluenceCleanerService:
    """
    Service class to clean Confluence pages by removing HTML tags and replacing HTML entities.
    """

    def clean_confluence_pages(self, pages: List[Document]) -> List[Document]:
        """
        Cleans the content of a list of Confluence pages by removing HTML tags and replacing HTML entities.
        Args:
            pages (List[Document]): List of Document objects representing Confluence pages.
        Returns:
            List[Document]: List of Document objects with cleaned content.
        Raises:
            Exception: If an error occurs during the cleaning process.
        """
        try:
            for page in pages:
                page = self.__remove_html_tags(page)
                page = self.__replace_html_entities(page)
            return pages
        except Exception as e:
            logger.error(f"Error cleaning confluence pages: {e}")
            raise e

    def __remove_html_tags(self, document: Document) -> Document:
        """
        Removes HTML tags from the content of the given Document.
        Args:
            document (Document): The Document from which HTML tags need to be removed.
        Returns:
            Document: The Document with HTML tags removed from its content.
        Raises:
            Exception: If an error occurs during the removal of HTML tags.
        """
        try:
            document.set_page_content(re.sub(r'<[^>]+>', ' ', document.get_page_content()))
            return document
        except Exception as e:
            logger.error(f"Error removing HTML tags: {e}")
            raise e

    def __replace_html_entities(self, document: Document) -> Document:
        """
        Replaces HTML entities in the content of the given Document with their corresponding characters.
        Args:
            document (Document): The Document in which HTML entities need to be replaced.
        Returns:
            Document: The Document with HTML entities replaced by their corresponding characters.
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
                document.set_page_content(document.get_page_content().replace(entity, char))
            return document
        except Exception as e:
            logger.error(f"Error replacing HTML entities: {e}")
            raise e
