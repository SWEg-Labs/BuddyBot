from abc import ABC, abstractmethod
from models.document import Document

class SimilaritySearchPort(ABC):
    @abstractmethod
    def similarity_search(self, user_input: str) -> list[Document]:
        pass
