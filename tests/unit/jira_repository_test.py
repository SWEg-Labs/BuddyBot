import pytest
from unittest.mock import MagicMock, patch
from requests.exceptions import RequestException
from datetime import datetime
import pytz

from models.loggingModels import PlatformLog, LoadingItems
from entities.issueEntity import IssueEntity
from repositories.jiraRepository import JiraRepository


# Verifica che il metodo get_base_url di JiraRepository restituisca l'URL base corretto
def test_get_base_url():
    # Arrange
    base_url = "https://jira.example.com"
    jira_repository = JiraRepository(base_url, "PROJ", 10, {})

    # Act
    result = jira_repository.get_base_url()

    # Assert
    assert result == base_url


# Verifica che il metodo load_jira_issues di JiraRepository restituisca correttamente le issues

@patch('requests.get')
def test_load_jira_issues(mock_get):
    # Arrange
    base_url = "https://jira.example.com"
    project_key = "PROJ"
    timeout = 10
    headers = {"Authorization": "Bearer token"}
    jira_repository = JiraRepository(base_url, project_key, timeout, headers)

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "issues": [
            {
                "id": "10001",
                "key": "PROJ-1",
                "fields": {
                    "summary": "Issue summary",
                    "description": "Detailed description of the issue",
                    "issuetype": {"name": "Bug", "description": "A problem which impairs or prevents the functions of the product."},
                    "project": {"id": "10000", "key": "PROJ", "name": "Project Name"},
                    "status": {"name": "Open", "description": "The issue is open and ready for the assignee to start work on it."},
                    "priority": {"name": "High", "description": "This problem will block progress."},
                    "assignee": {"name": "John Doe", "emailAddress": "john.doe@example.com", "displayName": "John Doe"},
                    "reporter": {"name": "Jane Smith", "emailAddress": "jane.smith@example.com", "displayName": "Jane Smith"},
                    "created": "2025-02-28T12:34:56.000+0000",
                    "updated": "2025-02-28T12:34:56.000+0000",
                    "attachment": [{"id": "10002", "filename": "example.txt", "content": "https://jira.example.com/secure/attachment/10002/example.txt"}]
                }
            }
        ]
    }
    mock_get.return_value = mock_response

    expected_issues = [
        IssueEntity(
            id="10001",
            key="PROJ-1",
            summary="Issue summary",
            description="Detailed description of the issue",
            issuetype={"name": "Bug", "description": "A problem which impairs or prevents the functions of the product."},
            project={"id": "10000", "key": "PROJ", "name": "Project Name"},
            status={"name": "Open", "description": "The issue is open and ready for the assignee to start work on it."},
            priority={"name": "High", "description": "This problem will block progress."},
            assignee={"name": "John Doe", "emailAddress": "john.doe@example.com", "displayName": "John Doe"},
            reporter={"name": "Jane Smith", "emailAddress": "jane.smith@example.com", "displayName": "Jane Smith"},
            created="2025-02-28T12:34:56.000+0000",
            updated="2025-02-28T12:34:56.000+0000",
            attachment=[{"id": "10002", "filename": "example.txt", "content": "https://jira.example.com/secure/attachment/10002/example.txt"}]
        )
    ]

    # Act
    log, issues = jira_repository.load_jira_issues()

    # Assert
    assert log.get_loading_items() == LoadingItems.JiraIssues
    assert log.get_outcome() is True
    assert len(issues) == len(expected_issues)
    assert issues[0].get_id() == expected_issues[0].get_id()


# Verifica che il metodo load_jira_issues di JiraRepository gestisca correttamente le eccezioni di richiesta

@patch('requests.get')
def test_load_jira_issues_request_exception(mock_get):
    # Arrange
    base_url = "https://jira.example.com"
    project_key = "PROJ"
    timeout = 10
    headers = {"Authorization": "Bearer token"}
    jira_repository = JiraRepository(base_url, project_key, timeout, headers)

    mock_get.side_effect = RequestException("Request error")

    # Act
    log, issues = jira_repository.load_jira_issues()

    # Assert
    assert log.get_loading_items() == LoadingItems.JiraIssues
    assert log.get_outcome() is False
    assert issues == []


# Verifica che il metodo load_jira_issues di JiraRepository gestisca correttamente le eccezioni generiche

@patch('requests.get')
def test_load_jira_issues_generic_exception(mock_get):
    # Arrange
    base_url = "https://jira.example.com"
    project_key = "PROJ"
    timeout = 10
    headers = {"Authorization": "Bearer token"}
    jira_repository = JiraRepository(base_url, project_key, timeout, headers)

    mock_get.side_effect = Exception("Generic error")

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        jira_repository.load_jira_issues()

    assert str(exc_info.value) == "Generic error"
