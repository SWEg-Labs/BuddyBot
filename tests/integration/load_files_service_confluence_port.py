from unittest.mock import MagicMock
from datetime import datetime, timedelta

from models.document import Document
from models.platform_log import PlatformLog
from models.platform import Platform
from ports.github_port import GitHubPort
from ports.jira_port import JiraPort
from ports.confluence_port import ConfluencePort
from ports.load_files_port import LoadFilesPort
from ports.save_loading_attempt_in_db_port import SaveLoadingAttemptInDbPort
from services.loadFilesService import LoadFilesService

# Verifica che il metodo load_confluence_pages di LoadFilesService chiami il metodo load_confluence_pages di ConfluencePort

def test_load_confluence_pages_calls_port_method():
    # Arrange
    mock_github_port = MagicMock(spec=GitHubPort)
    mock_jira_port = MagicMock(spec=JiraPort)
    mock_confluence_port = MagicMock(spec=ConfluencePort)
    mock_load_files_port = MagicMock(spec=LoadFilesPort)
    mock_save_loading_attempt_in_db_port = MagicMock(spec=SaveLoadingAttemptInDbPort)
    load_files_service = LoadFilesService(
        mock_github_port, mock_jira_port,
        mock_confluence_port, mock_load_files_port,
        mock_save_loading_attempt_in_db_port,
    )

    expected_result = (
        PlatformLog(
            platform=Platform.Confluence,
            timestamp=datetime.now() - timedelta(minutes=2),
            outcome=True
        ),
        [Document(page_content="doc1", metadata={"type": "html"})]
    )
    mock_confluence_port.load_confluence_pages.return_value = expected_result

    # Act
    result = load_files_service.load_confluence_pages()

    # Assert
    mock_confluence_port.load_confluence_pages.assert_called_once()
    assert result == expected_result