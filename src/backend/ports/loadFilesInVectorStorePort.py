from abc import ABC, abstractmethod

from models.document import Document
from models.loggingModels import VectorStoreLog

class LoadFilesInVectorStorePort(ABC):
    """
    Abstract base class that defines the interface for loading files into a vector store.
    This class should be inherited by any class that aims to implement
    the functionality of loading documents into a vector store.
    """

    @abstractmethod
    def load(self, documents: list[Document]) -> VectorStoreLog:
        """
        Abstract method to load a list of documents into a vector store.
        Args:
            documents (list[Document]): A list of Document objects to be loaded.
        Returns:
            VectorStoreLog: An instance of VectorStoreLog containing information about the load operation.
        """
        pass