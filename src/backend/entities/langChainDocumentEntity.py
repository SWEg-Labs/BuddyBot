from typing import Optional

class LangChainDocumentEntity:
    def __init__(self, page_content: str, metadata: Optional[dict] = None):
        self.page_content = page_content
        self.metadata = metadata if metadata is not None else {}

    def get_page_content(self) -> str:
        return self.page_content

    def get_metadata(self) -> dict:
        return self.metadata

    def set_page_content(self, page_content: str):
        self.page_content = page_content

    def set_metadata(self, metadata: dict):
        self.metadata = metadata

    def add_metadata(self, key: str, value):
        self.metadata[key] = value

    def remove_metadata(self, key: str):
        if key in self.metadata:
            del self.metadata[key]

    def __repr__(self) -> str:
        return f"Document(page_content={self.page_content!r}, metadata={self.metadata!r})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, LangChainDocumentEntity):
            return False
        return self.page_content == other.page_content and self.metadata == other.metadata