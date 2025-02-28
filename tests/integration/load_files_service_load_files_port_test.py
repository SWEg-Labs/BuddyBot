from unittest.mock import MagicMock
from datetime import datetime

from models.document import Document
from models.vectorStoreLog import VectorStoreLog
from services.loadFilesService import LoadFilesService
from ports.githubPort import GitHubPort
from ports.jiraPort import JiraPort
from ports.confluencePort import ConfluencePort
from ports.loadFilesPort import LoadFilesPort
from ports.saveLoadingAttemptInDbPort import SaveLoadingAttemptInDbPort

# Verifica che il metodo load_in_vector_store di LoadFilesService chiami il metodo load di LoadFilesPort

def test_load_calls_port_method():
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
        num_modifed_items=0,
        num_deleted_items=0
    )
    mock_load_files_port.load.return_value = vector_store_log

    # Act
    result = load_files_service.load_in_vector_store(documents)

    # Assert
    mock_load_files_port.load.assert_called_once_with(documents)
    assert result == "mocked_vector_store_log"