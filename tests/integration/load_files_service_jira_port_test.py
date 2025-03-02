from unittest.mock import MagicMock
from datetime import datetime, timedelta

from models.document import Document
from models.loggingModels import PlatformLog, LoadingItems
from services.loadFilesService import LoadFilesService
from services.confluenceCleanerService import ConfluenceCleanerService
from ports.gitHubPort import GitHubPort
from ports.jiraPort import JiraPort
from ports.confluencePort import ConfluencePort
from ports.loadFilesInVectorStorePort import LoadFilesInVectorStorePort
from ports.saveLoadingAttemptInDbPort import SaveLoadingAttemptInDbPort

# Verifica che il metodo load_jira_issues di LoadFilesService chiami il metodo load_jira_issues di JiraPort

def test_load_jira_issues_calls_port_method():
    # Arrange
    mock_github_port = MagicMock(spec=GitHubPort)
    mock_jira_port = MagicMock(spec=JiraPort)
    mock_confluence_port = MagicMock(spec=ConfluencePort)
    mock_load_files_in_vector_store_port = MagicMock(spec=LoadFilesInVectorStorePort)
    mock_save_loading_attempt_in_db_port = MagicMock(spec=SaveLoadingAttemptInDbPort)
    mock_confluence_cleaner_service = MagicMock(spec=ConfluenceCleanerService)
    load_files_service = LoadFilesService(
        mock_github_port, mock_jira_port,
        mock_confluence_port, mock_confluence_cleaner_service,
        mock_load_files_in_vector_store_port, mock_save_loading_attempt_in_db_port
    )

    expected_result = (
        PlatformLog(
            loading_items=LoadingItems.JiraIssues,
            timestamp=datetime(2025, 2, 28, 12, 34, 56) - timedelta(minutes=3),
            outcome=True
        ),
        [Document(page_content="doc1", metadata={"type": "text"})]
    )
    mock_jira_port.load_jira_issues.return_value = expected_result

    # Act
    result = load_files_service.load_jira_issues()

    # Assert
    mock_jira_port.load_jira_issues.assert_called_once()
    assert result == expected_result