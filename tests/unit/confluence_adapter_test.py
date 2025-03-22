import pytest
from unittest.mock import MagicMock

from adapters.confluenceAdapter import ConfluenceAdapter
from repositories.confluenceRepository import ConfluenceRepository


# Verifica che il metodo load_confluence_pages di ConfluenceAdapter gestisca correttamente le eccezioni

def test_load_confluence_pages_exception():
    # Arrange
    mock_confluence_repository = MagicMock(spec=ConfluenceRepository)
    confluence_adapter = ConfluenceAdapter(mock_confluence_repository)
    mock_confluence_repository.load_confluence_pages.side_effect = Exception("Error loading Confluence pages")

    # Act
    with pytest.raises(Exception) as exc_info:
        confluence_adapter.load_confluence_pages()

    # Assert
    assert str(exc_info.value) == "Error loading Confluence pages"


# Verifica che il metodo UTC_to_CET di ConfluenceAdapter gestisca correttamente le eccezioni

def test_utc_to_cet_exception():
    # Arrange
    mock_confluence_repository = MagicMock(spec=ConfluenceRepository)
    confluence_adapter = ConfluenceAdapter(mock_confluence_repository)
    invalid_timestamp = "invalid_timestamp"  # Passing an invalid timestamp to trigger an exception

    # Act
    with pytest.raises(Exception) as exc_info:
        confluence_adapter._ConfluenceAdapter__UTC_to_CET(invalid_timestamp)

    # Assert
    assert "time data 'invalid_timestamp' does not match format '%Y-%m-%dT%H:%M:%S.%fZ'" in str(exc_info.value)
