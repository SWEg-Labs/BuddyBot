from use_cases.loadFilesUseCase import LoadFilesUseCase
from utils.logger import logger

class LoadFilesController:
    """
    Controller class to manage file loading operations.
    """
    def __init__(self, load_files_use_case: LoadFilesUseCase):
        """
        Initializes the LoadFilesController with the given use case.
        Args:
            load_files_use_case (LoadFilesUseCase): Use case for loading files.
        """
        self.load_files_use_case = load_files_use_case

    def load(self):
        """
        Load files from various platforms to a vector store.
        """
        try:
            self.load_files_use_case.load()
        except Exception as e:
            logger.error(f"Error loading files: {e}")
            raise
