import pytest
from unittest.mock import MagicMock

from controllers.loadFilesController import LoadFilesController
from use_cases.loadFilesUseCase import LoadFilesUseCase


# Verifica che il metodo load di LoadFilesController gestisca correttamente le eccezioni

def test_load_handles_exception():
    # Arrange
    mock_load_files_use_case = MagicMock(spec=LoadFilesUseCase)
    mock_load_files_use_case.load.side_effect = Exception("Load error")
    load_files_controller = LoadFilesController(mock_load_files_use_case)

    # Act
    with pytest.raises(Exception) as exc_info:
        load_files_controller.load()

    # Assert
    assert str(exc_info.value) == "Load error"
