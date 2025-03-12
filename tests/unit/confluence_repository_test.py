import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
import pytz
from requests.exceptions import RequestException

from models.loggingModels import PlatformLog, LoadingItems
from entities.pageEntity import PageEntity
from repositories.confluenceRepository import ConfluenceRepository

# Verifica che il metodo get_base_url di ConfluenceRepository ritorni l'URL base corretto
def test_get_base_url():
    # Arrange
    base_url = "https://confluence.example.com"
    repository = ConfluenceRepository(base_url, "PROJECT_KEY", 30, {"Authorization": "Bearer token"})

    # Act
    result = repository.get_base_url()

    # Assert
    assert result == base_url

# Verifica che il metodo load_confluence_pages di ConfluenceRepository ritorni le pagine correttamente
@patch('requests.get')
def test_load_confluence_pages(mock_get):
    # Arrange
    base_url = "https://confluence.example.com"
    project_key = "PROJECT_KEY"
    timeout = 30
    headers = {"Authorization": "Bearer token"}
    repository = ConfluenceRepository(base_url, project_key, timeout, headers)

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [
            {
                "id": "12345",
                "type": "page",
                "title": "Example Page",
                "space": {"key": "SPACEKEY", "name": "Space Name", "type": "global"},
                "body": {"view": {"value": "<p>This is an example page content.</p>", "representation": "storage"}},
                "version": {"by": {"username": "john.doe", "displayName": "John Doe"}, "when": "2025-02-28T12:34:56.000+0000", "number": 1, "minorEdit": False},
                "status": "current",
                "ancestors": [],
                "extensions": {"position": "none"},
                "_links": {"webui": "/spaces/SPACEKEY/pages/12345/Example+Page", "self": "https://confluence.example.com/rest/api/content/12345"}
            }
        ]
    }
    mock_get.return_value = mock_response

    expected_pages = [
        PageEntity(
            id="12345",
            type="page",
            title="Example Page",
            space={"key": "SPACEKEY", "name": "Space Name", "type": "global"},
            body={"view": {"value": "<p>This is an example page content.</p>", "representation": "storage"}},
            version={"by": {"username": "john.doe", "displayName": "John Doe"}, "when": "2025-02-28T12:34:56.000+0000", "number": 1, "minorEdit": False},
            status="current",
            ancestors=[], extensions={"position": "none"},
            links={"webui": "/spaces/SPACEKEY/pages/12345/Example+Page", "self": "https://confluence.example.com/rest/api/content/12345"}
        )
    ]

    # Act
    log, pages = repository.load_confluence_pages()

    # Assert
    assert log.get_loading_items() == LoadingItems.ConfluencePages
    assert log.get_outcome() is True
    assert pages == expected_pages

# Verifica che il metodo load_confluence_pages di ConfluenceRepository gestisca correttamente le eccezioni di richiesta
@patch('requests.get')
def test_load_confluence_pages_request_exception(mock_get):
    # Arrange
    base_url = "https://confluence.example.com"
    project_key = "PROJECT_KEY"
    timeout = 30
    headers = {"Authorization": "Bearer token"}
    repository = ConfluenceRepository(base_url, project_key, timeout, headers)

    mock_get.side_effect = RequestException("Request error")

    # Act
    log, pages = repository.load_confluence_pages()

    # Assert
    assert log.get_loading_items() == LoadingItems.ConfluencePages
    assert log.get_outcome() is False
    assert pages == []

# Verifica che il metodo load_confluence_pages di ConfluenceRepository gestisca correttamente le eccezioni generiche
@patch('requests.get')
def test_load_confluence_pages_generic_exception(mock_get):
    # Arrange
    base_url = "https://confluence.example.com"
    project_key = "PROJECT_KEY"
    timeout = 30
    headers = {"Authorization": "Bearer token"}
    repository = ConfluenceRepository(base_url, project_key, timeout, headers)

    mock_get.side_effect = Exception("Generic error")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        repository.load_confluence_pages()

    assert str(exc_info.value) == "Generic error"
