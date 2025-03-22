import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import pytz

from models.document import Document
from models.loggingModels import PlatformLog, VectorStoreLog, LoadingAttempt, LoadingItems
from models.dbSaveOperationResponse import DbSaveOperationResponse
from services.loadFilesService import LoadFilesService
from services.confluenceCleanerService import ConfluenceCleanerService
from ports.gitHubPort import GitHubPort
from ports.jiraPort import JiraPort
from ports.confluencePort import ConfluencePort
from ports.loadFilesInVectorStorePort import LoadFilesInVectorStorePort
from ports.saveLoadingAttemptInDbPort import SaveLoadingAttemptInDbPort


# Verifica che il metodo load di LoadFilesService carichi correttamente i dati dai vari servizi e salvi i log di caricamento

def test_load_calls_all_methods_and_handles_exceptions():
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

    italy_tz = pytz.timezone('Europe/Rome')
    starting_timestamp = datetime.now(italy_tz)

    github_commits_log = PlatformLog(loading_items=LoadingItems.GitHubCommits, timestamp=starting_timestamp, outcome=True)
    github_files_log = PlatformLog(loading_items=LoadingItems.GitHubFiles, timestamp=starting_timestamp, outcome=True)
    jira_issues_log = PlatformLog(loading_items=LoadingItems.JiraIssues, timestamp=starting_timestamp, outcome=True)
    confluence_pages_log = PlatformLog(loading_items=LoadingItems.ConfluencePages, timestamp=starting_timestamp, outcome=True)

    github_commits = [Document(page_content="commit1", metadata={"type": "text", "date": "2023-10-01 10:00:00"})]
    github_files = [Document(page_content="file1", metadata={"type": "python", "path": "src/file1.py"})]
    jira_issues = [Document(page_content="issue1", metadata={"type": "text"})]
    confluence_pages = [Document(page_content="page1", metadata={"type": "html"})]
    cleaned_confluence_pages = [Document(page_content="cleaned_page1", metadata={"type": "html"})]

    vector_store_log = VectorStoreLog(timestamp=starting_timestamp, outcome=True, num_added_items=4, num_modified_items=0, num_deleted_items=0)
    db_save_response = DbSaveOperationResponse(success=True, message="Saved successfully")

    mock_github_port.load_github_commits.return_value = (github_commits_log, github_commits)
    mock_github_port.load_github_files.return_value = (github_files_log, github_files)
    mock_jira_port.load_jira_issues.return_value = (jira_issues_log, jira_issues)
    mock_confluence_port.load_confluence_pages.return_value = (confluence_pages_log, confluence_pages)
    mock_confluence_cleaner_service.clean_confluence_pages.return_value = cleaned_confluence_pages
    mock_load_files_in_vector_store_port.load.return_value = vector_store_log
    mock_save_loading_attempt_in_db_port.save_loading_attempt.return_value = db_save_response

    # Act
    load_files_service.load()

    # Assert
    mock_github_port.load_github_commits.assert_called_once()
    mock_github_port.load_github_files.assert_called_once()
    mock_jira_port.load_jira_issues.assert_called_once()
    mock_confluence_port.load_confluence_pages.assert_called_once()
    mock_confluence_cleaner_service.clean_confluence_pages.assert_called_once_with(confluence_pages)
    mock_load_files_in_vector_store_port.load.assert_called_once_with(github_commits + github_files + jira_issues + cleaned_confluence_pages)
    mock_save_loading_attempt_in_db_port.save_loading_attempt.assert_called_once()


# Verifica che il metodo load di LoadFilesService gestisca correttamente le eccezioni

def test_load_handles_exception():
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

    mock_github_port.load_github_commits.side_effect = Exception("GitHub commits error")

    # Act
    with pytest.raises(Exception) as exc_info:
        load_files_service.load()

    # Assert
    assert str(exc_info.value) == "GitHub commits error"


# Verifica che il metodo load di LoadFilesService sollevi un'eccezione se il salvataggio nel database fallisce

def test_load_raises_exception_if_db_save_fails():
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

    italy_tz = pytz.timezone('Europe/Rome')
    starting_timestamp = datetime.now(italy_tz)

    github_commits_log = PlatformLog(loading_items=LoadingItems.GitHubCommits, timestamp=starting_timestamp, outcome=True)
    github_files_log = PlatformLog(loading_items=LoadingItems.GitHubFiles, timestamp=starting_timestamp, outcome=True)
    jira_issues_log = PlatformLog(loading_items=LoadingItems.JiraIssues, timestamp=starting_timestamp, outcome=True)
    confluence_pages_log = PlatformLog(loading_items=LoadingItems.ConfluencePages, timestamp=starting_timestamp, outcome=True)

    github_commits = [Document(page_content="commit1", metadata={"type": "text", "date": "2023-10-01 10:00:00"})]
    github_files = [Document(page_content="file1", metadata={"type": "python", "path": "src/file1.py"})]
    jira_issues = [Document(page_content="issue1", metadata={"type": "text"})]
    confluence_pages = [Document(page_content="page1", metadata={"type": "html"})]
    cleaned_confluence_pages = [Document(page_content="cleaned_page1", metadata={"type": "html"})]

    vector_store_log = VectorStoreLog(timestamp=starting_timestamp, outcome=True, num_added_items=4, num_modified_items=0, num_deleted_items=0)
    db_save_response = DbSaveOperationResponse(success=False, message="Connection to the database failed")

    mock_github_port.load_github_commits.return_value = (github_commits_log, github_commits)
    mock_github_port.load_github_files.return_value = (github_files_log, github_files)
    mock_jira_port.load_jira_issues.return_value = (jira_issues_log, jira_issues)
    mock_confluence_port.load_confluence_pages.return_value = (confluence_pages_log, confluence_pages)
    mock_confluence_cleaner_service.clean_confluence_pages.return_value = cleaned_confluence_pages
    mock_load_files_in_vector_store_port.load.return_value = vector_store_log
    mock_save_loading_attempt_in_db_port.save_loading_attempt.return_value = db_save_response

    # Act
    with pytest.raises(Exception) as exc_info:
        load_files_service.load()

    # Assert
    assert str(exc_info.value) == "Failed to save loading attempt in Postgres database: Connection to the database failed. Details: Connection to the database failed"


# Verifica che il metodo load_github_commits di LoadFilesService gestisca correttamente le eccezioni

def test_load_github_commits_handles_exception():
    # Arrange
    mock_github_port = MagicMock(spec=GitHubPort)
    load_files_service = LoadFilesService(
        mock_github_port, MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()
    )

    mock_github_port.load_github_commits.side_effect = Exception("GitHub commits error")

    # Act
    with pytest.raises(Exception) as exc_info:
        load_files_service.load_github_commits()

    # Assert
    assert str(exc_info.value) == "GitHub commits error"


# Verifica che il metodo load_github_files di LoadFilesService gestisca correttamente le eccezioni

def test_load_github_files_handles_exception():
    # Arrange
    mock_github_port = MagicMock(spec=GitHubPort)
    load_files_service = LoadFilesService(
        mock_github_port, MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()
    )

    mock_github_port.load_github_files.side_effect = Exception("GitHub files error")

    # Act
    with pytest.raises(Exception) as exc_info:
        load_files_service.load_github_files()

    # Assert
    assert str(exc_info.value) == "GitHub files error"


# Verifica che il metodo load_jira_issues di LoadFilesService gestisca correttamente le eccezioni

def test_load_jira_issues_handles_exception():
    # Arrange
    mock_jira_port = MagicMock(spec=JiraPort)
    load_files_service = LoadFilesService(
        MagicMock(), mock_jira_port, MagicMock(), MagicMock(), MagicMock(), MagicMock()
    )

    mock_jira_port.load_jira_issues.side_effect = Exception("Jira issues error")

    # Act
    with pytest.raises(Exception) as exc_info:
        load_files_service.load_jira_issues()

    # Assert
    assert str(exc_info.value) == "Jira issues error"


# Verifica che il metodo load_confluence_pages di LoadFilesService gestisca correttamente le eccezioni

def test_load_confluence_pages_handles_exception():
    # Arrange
    mock_confluence_port = MagicMock(spec=ConfluencePort)
    load_files_service = LoadFilesService(
        MagicMock(), MagicMock(), mock_confluence_port, MagicMock(), MagicMock(), MagicMock()
    )

    mock_confluence_port.load_confluence_pages.side_effect = Exception("Confluence pages error")

    # Act
    with pytest.raises(Exception) as exc_info:
        load_files_service.load_confluence_pages()

    # Assert
    assert str(exc_info.value) == "Confluence pages error"


# Verifica che il metodo get_github_files_new_metadata di LoadFilesService aggiorni correttamente i metadati
# "last_update" e "creation_date" dei file di GitHub

def test_get_github_files_new_metadata_updates_metadata_correctly():
    # Arrange
    mock_github_port = MagicMock(spec=GitHubPort)
    load_files_service = LoadFilesService(
        mock_github_port, MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()
    )

    github_files = [
        Document(page_content="file1", metadata={"path": "src/file1.py"}),
        Document(page_content="file2", metadata={"path": "src/file2.py"}),
    ]

    github_commits = [
        Document(page_content="commit1", metadata={
            "date": "2023-10-01 10:00:00",
            "files": [
                "- src/file1.py (Status: added, Changes: 10)",
                "- src/file2.py (Status: modified, Changes: 5)"
            ]
        }),
        Document(page_content="commit2", metadata={
            "date": "2023-10-02 12:00:00",
            "files": [
                "- src/file1.py (Status: renamed, Changes: 0)"
            ]
        }),
    ]

    # Act
    updated_files = load_files_service.get_github_files_new_metadata(github_files, github_commits)

    # Assert
    assert updated_files[0].get_metadata()["last_update"] == "2023-10-02 12:00:00"
    assert updated_files[0].get_metadata()["creation_date"] == "2023-10-02 12:00:00"
    assert updated_files[1].get_metadata()["last_update"] == "2023-10-01 10:00:00"
    assert "creation_date" not in updated_files[1].get_metadata()  # There are no commits that added this file


# Verifica che il metodo get_github_files_new_metadata di LoadFilesService gestisca correttamente l'eccezione di path mancante
# nei metadati dei file di GitHub

def test_get_github_files_new_metadata_handles_missing_path():
    # Arrange
    mock_github_port = MagicMock(spec=GitHubPort)
    load_files_service = LoadFilesService(
        mock_github_port, MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()
    )

    github_files = [
        Document(page_content="file1", metadata={}),  # Missing "path"
    ]

    github_commits = [
        Document(page_content="commit1", metadata={
            "date": "2023-10-01 10:00:00",
            "files": [
                "- src/file1.py (Status: added, Changes: 10)"
            ]
        }),
    ]

    # Act
    with pytest.raises(ValueError) as exc_info:
        load_files_service.get_github_files_new_metadata(github_files, github_commits)

    # Assert
    assert str(exc_info.value) == "File path not found in GitHub file metadata."


# Verifica che il metodo get_github_files_new_metadata di LoadFilesService gestisca correttamente le eccezioni di formato
# della data errato o di data assente nei metadati dei commit di GitHub

def test_get_github_files_new_metadata_handles_invalid_date_exception():
    # Arrange
    mock_github_port = MagicMock(spec=GitHubPort)
    load_files_service = LoadFilesService(
        mock_github_port, MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()
    )

    github_files = [
        Document(page_content="file1", metadata={"path": "src/file1.py"}),
    ]

    github_commits = [
        Document(page_content="commit1", metadata={
            "date": "invalid-date",
            "files": [
                "- src/file1.py (Status: added, Changes: 10)"
            ]
        }),
    ]

    # Act
    with pytest.raises(ValueError) as exc_info:
        load_files_service.get_github_files_new_metadata(github_files, github_commits)

    # Assert
    assert str(exc_info.value) == "Invalid date format in GitHub commit: invalid-date"


# Verifica che il metodo clean_confluence_pages di LoadFilesService gestisca correttamente le eccezioni

def test_clean_confluence_pages_handles_exception():
    # Arrange
    mock_confluence_cleaner_service = MagicMock(spec=ConfluenceCleanerService)
    load_files_service = LoadFilesService(
        MagicMock(), MagicMock(), MagicMock(), mock_confluence_cleaner_service, MagicMock(), MagicMock()
    )

    mock_confluence_cleaner_service.clean_confluence_pages.side_effect = Exception("Clean Confluence pages error")

    # Act
    with pytest.raises(Exception) as exc_info:
        load_files_service.clean_confluence_pages([])

    # Assert
    assert str(exc_info.value) == "Clean Confluence pages error"


# Verifica che il metodo load_in_vector_store di LoadFilesService gestisca correttamente le eccezioni

def test_load_in_vector_store_handles_exception():
    # Arrange
    mock_load_files_in_vector_store_port = MagicMock(spec=LoadFilesInVectorStorePort)
    load_files_service = LoadFilesService(
        MagicMock(), MagicMock(), MagicMock(), MagicMock(), mock_load_files_in_vector_store_port, MagicMock()
    )

    mock_load_files_in_vector_store_port.load.side_effect = Exception("Load in vector store error")

    # Act
    with pytest.raises(Exception) as exc_info:
        load_files_service.load_in_vector_store([])

    # Assert
    assert str(exc_info.value) == "Load in vector store error"


# Verifica che il metodo save_loading_attempt_in_db di LoadFilesService gestisca correttamente le eccezioni

def test_save_loading_attempt_in_db_handles_exception():
    # Arrange
    mock_save_loading_attempt_in_db_port = MagicMock(spec=SaveLoadingAttemptInDbPort)
    load_files_service = LoadFilesService(
        MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock(), mock_save_loading_attempt_in_db_port
    )

    mock_save_loading_attempt_in_db_port.save_loading_attempt.side_effect = Exception("Save loading attempt in DB error")

    # Act
    with pytest.raises(Exception) as exc_info:
        load_files_service.save_loading_attempt_in_db(LoadingAttempt([], VectorStoreLog(datetime.now(), True, 0, 0, 0), datetime.now()))

    # Assert
    assert str(exc_info.value) == "Save loading attempt in DB error"


# Verifica che il metodo save_loading_attempt_in_txt di LoadFilesService gestisca correttamente le eccezioni

def test_save_loading_attempt_in_txt_handles_exception():
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
        starting_timestamp=datetime(2025, 2, 28, 12, 34, 56) - timedelta(minutes=6)
    )

    with patch('utils.logger.file_logger.info') as mock_file_logger_info:
        mock_file_logger_info.side_effect = Exception("File logger error")

        # Act
        with pytest.raises(Exception) as exc_info:
            load_files_service.save_loading_attempt_in_txt(loading_attempt)

        # Assert
        assert str(exc_info.value) == "File logger error"
