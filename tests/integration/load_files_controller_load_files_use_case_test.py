from unittest.mock import MagicMock
from controllers.loadFilesController import LoadFilesController
from use_cases.loadFilesUseCase import LoadFilesUseCase

# Verifica che il metodo load di LoadFilesController chiami il metodo load di LoadFilesUseCase

def test_load_calls_use_case_method():
    # Arrange
    mock_load_files_use_case = MagicMock(spec=LoadFilesUseCase)
    load_files_controller = LoadFilesController(mock_load_files_use_case)

    # Act
    load_files_controller.load()

    # Assert
    mock_load_files_use_case.load.assert_called_once()
