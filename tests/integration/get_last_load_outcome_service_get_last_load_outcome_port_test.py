from unittest.mock import MagicMock

from models.lastLoadOutcome import LastLoadOutcome
from services.getLastLoadOutcomeService import GetLastLoadOutcomeService
from ports.getLastLoadOutcomePort import GetLastLoadOutcomePort


# Verifica che il metodo get_last_load_outcome di GetLastLoadOutcomeService chiami il metodo get_last_load_outcome di GetLastLoadOutcomePort

def test_get_last_load_outcome_calls_port_method():
    # Arrange
    mock_get_last_load_outcome_port = MagicMock(spec=GetLastLoadOutcomePort)
    get_last_load_outcome_service = GetLastLoadOutcomeService(mock_get_last_load_outcome_port)
    expected_outcome = LastLoadOutcome.TRUE
    mock_get_last_load_outcome_port.get_last_load_outcome.return_value = expected_outcome

    # Act
    result = get_last_load_outcome_service.get_last_load_outcome()

    # Assert
    mock_get_last_load_outcome_port.get_last_load_outcome.assert_called_once()
    assert result == expected_outcome
