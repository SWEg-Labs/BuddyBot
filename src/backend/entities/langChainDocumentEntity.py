from typing import Optional

class LangChainDocumentEntity:
    def __init__(self, content: str, metadata: Optional[dict] = None):
        self.content = content
        self.metadata = metadata if metadata is not None else {}

    def get_content(self) -> str:
        return self.content

    def get_metadata(self) -> dict:
        return self.metadata

    def set_content(self, content: str):
        self.content = content

    def set_metadata(self, metadata: dict):
        self.metadata = metadata

    def add_metadata(self, key: str, value):
        self.metadata[key] = value

    def remove_metadata(self, key: str):
        if key in self.metadata:
            del self.metadata[key]

    def __repr__(self) -> str:
        return f"Document(content={self.content!r}, metadata={self.metadata!r})"