from unittest.mock import MagicMock
from datetime import datetime, timedelta
from models.document import Document
from models.platformLog import PlatformLog
from adapters.confluenceAdapter import ConfluenceAdapter
from repositories.confluenceRepository import ConfluenceRepository
from entities.pageEntity import PageEntity

def test_load_confluence_pages_calls_repository_method():
    # Arrange
    mock_confluence_repository = MagicMock(spec=ConfluenceRepository)
    confluence_adapter = ConfluenceAdapter(mock_confluence_repository)

    expected_result = (
        PlatformLog(
            platform="Confluence",
            timestamp=datetime.now() - timedelta(minutes=5),
            outcome=True
        ),
        [
            Document(
                page_content="<p>This is an example page content.</p>",  # Contenuto del campo storage.value
                metadata={
                    "title": "Example Page",
                    "space": "Space Name"
                    "created_by": "John Doe",
                    "created_date": "2025-02-28T12:34:56.000+0000",
                    "url": "https://confluence.example.com/spaces/SPACEKEY/pages/12345/Example+Page", # Unione dei due campi dentro "links"
                    "id": "12345",
                }
            )
        ]
    )

    repository_return_value = (
        PlatformLog(
            platform="Confluence",
            timestamp=datetime.now() - timedelta(minutes=5),
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
                    "storage": {
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
