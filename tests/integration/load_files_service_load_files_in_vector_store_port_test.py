from unittest.mock import MagicMock
from datetime import datetime

from models.document import Document
from models.loggingModels import VectorStoreLog
from services.loadFilesService import LoadFilesService
from services.confluenceCleanerService import ConfluenceCleanerService
from ports.gitHubPort import GitHubPort
from ports.jiraPort import JiraPort
from ports.confluencePort import ConfluencePort
from ports.loadFilesInVectorStorePort import LoadFilesInVectorStorePort
from ports.saveLoadingAttemptInDbPort import SaveLoadingAttemptInDbPort


# Verifica che il metodo load_in_vector_store di LoadFilesService chiami il metodo load di LoadFilesInVectorStorePort

def test_load_calls_port_method():
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
    documents = [
        Document(page_content="doc1", metadata={"type": "text"}),
        Document(page_content="doc2", metadata={"type": "python"}),
        Document(page_content="doc3", metadata={"type": "text"}),
        Document(page_content="doc4", metadata={"type": "html"}),
    ]
    vector_store_log = VectorStoreLog(
        timestamp=datetime(2025, 2, 28, 12, 34, 56),
        outcome=True,
        num_added_items=4,
        num_modified_items=0,
        num_deleted_items=0
    )
    mock_load_files_in_vector_store_port.load.return_value = vector_store_log

    # Act
    result = load_files_service.load_in_vector_store(documents)

    # Assert
    mock_load_files_in_vector_store_port.load.assert_called_once_with(documents)
    assert result == vector_store_log
