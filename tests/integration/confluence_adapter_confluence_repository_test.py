from unittest.mock import MagicMock
from datetime import datetime, timedelta
from models.document import Document
from models.loggingModels import PlatformLog, LoadingItems
from adapters.confluenceAdapter import ConfluenceAdapter
from repositories.confluenceRepository import ConfluenceRepository
from entities.pageEntity import PageEntity


# Verifica che il metodo load_confluence_pages di ConfluenceAdapter chiami il metodo load_confluence_pages di ConfluenceRepository

def test_load_confluence_pages_calls_repository_method():
    # Arrange
    mock_confluence_repository = MagicMock(spec=ConfluenceRepository)
    confluence_adapter = ConfluenceAdapter(mock_confluence_repository)

    mock_confluence_repository.get_base_url.return_value = "https://confluence.example.com"

    expected_result = (
        PlatformLog(
            loading_items=LoadingItems.ConfluencePages,
            timestamp=datetime(2025, 2, 28, 12, 34, 56) - timedelta(minutes=5),
            outcome=True
        ),
        [
            Document(
                page_content="<p>This is an example page content.</p>",  # Contenuto del campo storage.value
                metadata={
                    "title": "Example Page",
                    "space": "Space Name",
                    "created_by": "John Doe",
                    "item_type": "Confluence Page",
                    "creation_date": "2025-02-28T12:34:56.000+0000",
                    "url": "https://confluence.example.com/spaces/SPACEKEY/pages/12345/Example+Page", # Unione dei due campi dentro "links"
                    "id": "12345",
                }
            )
        ]
    )

    repository_return_value = (
        PlatformLog(
            loading_items=LoadingItems.ConfluencePages,
            timestamp=datetime(2025, 2, 28, 12, 34, 56) - timedelta(minutes=5),
            outcome=True
        ),
        [
            PageEntity(
                id="12345",
                type="page",
                title="Example Page",
                space={
                    "key": "SPACEKEY",
                    "name": "Space Name",
                    "type": "global"
                },
                body={
                    "view": {
                        "value": "<p>This is an example page content.</p>",
                        "representation": "storage"
                    }
                },
                version={
                    "by": {
                        "username": "john.doe",
                        "displayName": "John Doe"
                    },
                    "when": "2025-02-28T12:34:56.000+0000",
                    "number": 1,
                    "minorEdit": False
                },
                status="current",
                ancestors=[],
                extensions={
                    "position": "none"
                },
                links={
                    "webui": "/spaces/SPACEKEY/pages/12345/Example+Page",
                    "self": "https://confluence.example.com/rest/api/content/12345"
                }
            )
        ]
    )

    mock_confluence_repository.load_confluence_pages.return_value = repository_return_value

    # Act
    result = confluence_adapter.load_confluence_pages()

    # Assert
    mock_confluence_repository.load_confluence_pages.assert_called_once()
    assert result == expected_result
