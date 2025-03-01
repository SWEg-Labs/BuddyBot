from unittest.mock import MagicMock
from datetime import datetime, timedelta

from models.loggingModels import LoadingAttempt, VectorStoreLog, PlatformLog, LoadingItems
from models.dbSaveOperationResponse import DbSaveOperationResponse
from services.loadFilesService import LoadFilesService
from services.confluenceCleanerService import ConfluenceCleanerService
from ports.gitHubPort import GitHubPort
from ports.jiraPort import JiraPort
from ports.confluencePort import ConfluencePort
from ports.loadFilesInVectorStorePort import LoadFilesInVectorStorePort
from ports.saveLoadingAttemptInDbPort import SaveLoadingAttemptInDbPort

# Verifica che il metodo save_loading_attempt_in_db di LoadFilesService chiami il metodo save_loading_attempt di SaveLoadingAttemptInDbPort

def test_save_loading_attempt_in_db_calls_port_method():
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
    platform_logs = [
        PlatformLog(loading_items=LoadingItems.GitHubCommits, timestamp=datetime(2025, 2, 28, 12, 34, 56) - timedelta(minutes=5), outcome=True),
        PlatformLog(loading_items=LoadingItems.GitHubFiles, timestamp=datetime(2025, 2, 28, 12, 34, 56) - timedelta(minutes=4), outcome=True),
        PlatformLog(loading_items=LoadingItems.JiraIssues, timestamp=datetime(2025, 2, 28, 12, 34, 56) - timedelta(minutes=3), outcome=True),
        PlatformLog(loading_items=LoadingItems.ConfluencePages, timestamp=datetime(2025, 2, 28, 12, 34, 56) - timedelta(minutes=2), outcome=True),
    ]
    vector_store_log = VectorStoreLog(
        timestamp=datetime(2025, 2, 28, 12, 34, 56),
        outcome=True,
        num_added_items=4,
        num_modified_items=0,
        num_deleted_items=0,
    )
    loading_attempt = LoadingAttempt(
        platform_logs=platform_logs,
        vector_store_log=vector_store_log,
    )
    db_save_response = DbSaveOperationResponse(success=True, message="Saved successfully")
    mock_save_loading_attempt_in_db_port.save_loading_attempt.return_value = db_save_response

    # Act
    result = load_files_service.save_loading_attempt_in_db(loading_attempt)

    # Assert
    mock_save_loading_attempt_in_db_port.save_loading_attempt.assert_called_once_with(loading_attempt)
    assert result == db_save_response