from unittest.mock import MagicMock
from models.document import Document
from services.loadFilesService import LoadFilesService
from services.confluenceCleanerService import ConfluenceCleanerService
from ports.gitHubPort import GitHubPort
from ports.jiraPort import JiraPort
from ports.confluencePort import ConfluencePort
from ports.loadFilesInVectorStorePort import LoadFilesInVectorStorePort
from ports.saveLoadingAttemptInDbPort import SaveLoadingAttemptInDbPort


# Verifica che il metodo clean_confluence_pages di LoadFilesService chiami il metodo clean_confluence_pages di ConfluenceCleanerService

def test_clean_confluence_pages_calls_cleaner_service_method():
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
    pages = [
        Document(page_content="<html>doc1 &agrave; &egrave; &igrave; &ograve; &ugrave; &quot; &Egrave;</html>", metadata={"id": 1}),
        Document(page_content="<html>doc2 &agrave; &egrave; &igrave; &ograve; &ugrave; &quot; &Egrave;</html>", metadata={"id": 2}),
    ]
    cleaned_pages = [
        Document(page_content="doc1 à è ì ò ù \" È", metadata={"id": 1}),
        Document(page_content="doc2 à è ì ò ù \" È", metadata={"id": 2}),
    ]
    mock_confluence_cleaner_service.clean_confluence_pages.return_value = cleaned_pages

    # Act
    result = load_files_service.clean_confluence_pages(pages)

    # Assert
    mock_confluence_cleaner_service.clean_confluence_pages.assert_called_once_with(pages)
    assert result == cleaned_pages
