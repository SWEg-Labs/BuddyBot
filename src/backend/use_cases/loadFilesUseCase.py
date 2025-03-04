from abc import ABC, abstractmethod

class LoadFilesUseCase(ABC):
    """
    Abstract base class for loading files use case.
    This class defines the interface for loading files from various platforms to a vector store.
    """

    @abstractmethod
    def load(self):
        """
        Abstract method to load files from various platforms to a vector store.
        This method should be implemented by subclasses to define the specific loading logic.
        """
        pass
