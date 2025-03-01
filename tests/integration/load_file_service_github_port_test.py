from unittest.mock import MagicMock
from datetime import datetime, timedelta

from models.document import Document
from models.loggingModels import PlatformLog, LoadingItems
from ports.gitHubPort import GitHubPort
from ports.jiraPort import JiraPort
from ports.confluencePort import ConfluencePort
from ports.loadFilesInVectorStorePort import LoadFilesInVectorStorePort
from ports.saveLoadingAttemptInDbPort import SaveLoadingAttemptInDbPort
from services.confluenceCleanerService import ConfluenceCleanerService
from services.loadFilesService import LoadFilesService


# Verifica che il metodo load_github_commits di LoadFilesService chiami il metodo load_github_commits di GitHubPort

def test_load_github_commits_calls_port_method():
    # Arrange
    mock_github_port = MagicMock(spec=GitHubPort)
    mock_jira_port = MagicMock(spec=JiraPort)
    mock_confluence_port = MagicMock(spec=ConfluencePort)
    mock_load_files_in_vector_store_port = MagicMock(spec=LoadFilesInVectorStorePort)
    mock_save_loading_attempt_in_db_port = MagicMock(spec=SaveLoadingAttemptInDbPort)
    mock_confluence_cleaner_service = MagicMock(spec=ConfluenceCleanerService)
    load_files_service = LoadFilesService(
        mock_github_port, mock_jira_port,
        mock_confluence_port, mock_load_files_in_vector_store_port,
        mock_save_loading_attempt_in_db_port, mock_confluence_cleaner_service
    )

    expected_result = (
        PlatformLog(
            loading_items=LoadingItems.GitHubCommits,
            timestamp=datetime(2025, 2, 28, 12, 34, 56) - timedelta(minutes=5),
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
    mock_load_files_in_vector_store_port = MagicMock(spec=LoadFilesInVectorStorePort)
    mock_save_loading_attempt_in_db_port = MagicMock(spec=SaveLoadingAttemptInDbPort)
    mock_confluence_cleaner_service = MagicMock(spec=ConfluenceCleanerService)
    load_files_service = LoadFilesService(
        mock_github_port, mock_jira_port,
        mock_confluence_port, mock_load_files_in_vector_store_port,
        mock_save_loading_attempt_in_db_port, mock_confluence_cleaner_service
    )

    expected_result = (
        PlatformLog(
            loading_items=LoadingItems.GitHubFiles,
            timestamp=datetime(2025, 2, 28, 12, 34, 56) - timedelta(minutes=4),
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