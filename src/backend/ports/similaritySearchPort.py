from abc import ABC, abstractmethod

from models.document import Document
from models.question import Question

class SimilaritySearchPort(ABC):
    """
    Abstract base class for performing similarity searches.
    This class defines the interface for similarity search operations, which should be implemented by any concrete class that inherits from it.
    """

    @abstractmethod
    def similarity_search(self, user_input: Question) -> list[Document]:
        """
        Perform a similarity search based on the given user input.
        Args:
            user_input (Question): The input question for which similar documents are to be searched.
        Returns:
            list[Document]: A list of documents that are similar to the user input.
        """
        pass
