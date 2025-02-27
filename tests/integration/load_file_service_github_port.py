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
from services.load_files_service import LoadFilesService


# Verifica che il metodo load_github_commits di LoadFilesService chiami il metodo load_github_commits di GitHubPort

def test_load_github_commits_calls_port_method():
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
            platform=Platform.GitHub,
            timestamp=datetime.now() - timedelta(minutes=5),
            outcome=True
        ),
        [Document(page_content="doc1", metadata={"type": "text"})]
    )
    mock_github_port.load_github_commits.return_value = expected_result

    # Act
    result = load_files_service.load_github_commits()

    # Assert
    mock_github_port.load_github_commits.assert_called_once()
    assert result == expected_result


# Verifica che il metodo load_github_files di LoadFilesService chiami il metodo load_github_files di GitHubPort

def test_load_github_files_calls_port_method():
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
            platform=Platform.GitHub,
            timestamp=datetime.now() - timedelta(minutes=4),
            outcome=True
        ),
        [Document(page_content="doc1", metadata={"type": "python"})]
    )
    mock_github_port.load_github_files.return_value = expected_result

    # Act
    result = load_files_service.load_github_files()

    # Assert
    mock_github_port.load_github_files.assert_called_once()
    assert result == expected_result