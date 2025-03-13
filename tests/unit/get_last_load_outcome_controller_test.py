import pytest
from unittest.mock import MagicMock

from controllers.getLastLoadOutcomeController import GetLastLoadOutcomeController
from use_cases.getLastLoadOutcomeUseCase import GetLastLoadOutcomeUseCase


# Verifica che il metodo get_last_load_outcome di GetLastLoadOutcomeController gestisca correttamente le eccezioni

def test_get_last_load_outcome_exception():
    # Arrange
    mock_get_last_load_outcome_use_case = MagicMock(spec=GetLastLoadOutcomeUseCase)
    get_last_load_outcome_controller = GetLastLoadOutcomeController(mock_get_last_load_outcome_use_case)
    mock_get_last_load_outcome_use_case.get_last_load_outcome.side_effect = Exception("Test exception")

    # Act
    with pytest.raises(Exception) as exc_info:
        get_last_load_outcome_controller.get_last_load_outcome()

    # Assert
    assert str(exc_info.value) == "Test exception"
