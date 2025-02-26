from abc import ABC, abstractmethod
from models.document import Document
from models.question import Question

class SimilaritySearchPort(ABC):
    @abstractmethod
    def similarity_search(self, user_input: Question) -> list[Document]:
        pass
