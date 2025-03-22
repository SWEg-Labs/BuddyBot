from beartype.typing import Optional

from utils.beartype_personalized import beartype_personalized

@beartype_personalized
class ChromaDocumentEntity:
    def __init__(self, page_content: str, metadata: Optional[dict] = None):
        self.__page_content = page_content
        self.__metadata = metadata if metadata is not None else {}

    def get_page_content(self) -> str:
        return self.__page_content

    def get_metadata(self) -> dict:
        return self.__metadata

    def set_page_content(self, page_content: str):
        self.__page_content = page_content

    def set_metadata(self, metadata: dict):
        self.__metadata = metadata

    def add_metadata(self, key: str, value):
        self.__metadata[key] = value

    def remove_metadata(self, key: str):
        if key in self.__metadata:
            del self.__metadata[key]

    def __repr__(self) -> str:
        return f"Document(page_content={self.__page_content!r}, metadata={self.__metadata!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, ChromaDocumentEntity):
            return False
        return self.__page_content == other.get_page_content() and self.__metadata == other.get_metadata()
