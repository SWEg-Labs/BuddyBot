from unittest.mock import MagicMock

from dto.lastLoadOutcomeDTO import LastLoadOutcomeDTO
from models.lastLoadOutcome import LastLoadOutcome
from controllers.getLastLoadOutcomeController import GetLastLoadOutcomeController
from use_cases.getLastLoadOutcomeUseCase import GetLastLoadOutcomeUseCase


# Verifica che il metodo get_last_load_outcome di GetLastLoadOutcomeController chiami il metodo get_last_load_outcome di GetLastLoadOutcomeUseCase

def test_get_last_load_outcome_calls_use_case_method():
    # Arrange
    mock_get_last_load_outcome_use_case = MagicMock(spec=GetLastLoadOutcomeUseCase)
    get_last_load_outcome_controller = GetLastLoadOutcomeController(mock_get_last_load_outcome_use_case)
    use_case_outcome = LastLoadOutcome.TRUE
    mock_get_last_load_outcome_use_case.get_last_load_outcome.return_value = use_case_outcome
    expected_outcome = LastLoadOutcomeDTO.TRUE

    # Act
    result = get_last_load_outcome_controller.get_last_load_outcome()

    # Assert
    mock_get_last_load_outcome_use_case.get_last_load_outcome.assert_called_once()
    assert result == expected_outcome
