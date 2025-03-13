import pytest
from unittest.mock import MagicMock
from models.lastLoadOutcome import LastLoadOutcome
from services.getLastLoadOutcomeService import GetLastLoadOutcomeService
from ports.getLastLoadOutcomePort import GetLastLoadOutcomePort


# Verifica che il metodo get_last_load_outcome di GetLastLoadOutcomeService gestisca correttamente le eccezioni

def test_get_last_load_outcome_exception():
    # Arrange
    mock_get_last_load_outcome_port = MagicMock(spec=GetLastLoadOutcomePort)
    get_last_load_outcome_service = GetLastLoadOutcomeService(mock_get_last_load_outcome_port)
    mock_get_last_load_outcome_port.get_last_load_outcome.side_effect = Exception("Port error")

    # Act
    with pytest.raises(Exception) as exc_info:
        get_last_load_outcome_service.get_last_load_outcome()

    # Assert
    assert str(exc_info.value) == "Port error"
