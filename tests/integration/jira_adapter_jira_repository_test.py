from unittest.mock import MagicMock
from datetime import datetime

from models.document import Document
from models.loggingModels import PlatformLog, LoadingItems
from adapters.jiraAdapter import JiraAdapter
from repositories.jiraRepository import JiraRepository
from entities.issueEntity import IssueEntity

# Verifica che il metodo load_jira_issues di JiraAdapter chiami il metodo load_jira_issues di JiraRepository

def test_load_jira_issues_calls_repository_method():
    # Arrange
    mock_jira_repository = MagicMock(spec=JiraRepository)
    jira_adapter = JiraAdapter(mock_jira_repository)

    mock_jira_repository.get_base_url.return_value = "https://jira.example.com"

    expected_result = (
        PlatformLog(
            loading_items=LoadingItems.JiraIssues,
            timestamp=datetime(2025, 2, 28, 12, 34, 56),
            outcome=True
        ),
        [
            Document(
                page_content="Issue summary",  # Contenuto del campo summary
                metadata={
                    "project": "Project Name",
                    "status": "Open",
                    "assignee": "John Doe",
                    "priority": "High",
                    "type": "Bug",
                    "item_type": "Jira Issue",
                    "creation_date": "2025-02-28T12:34:56.000+0000",
                    "url": "https://jira.example.com/browse/PROJ-1", # issue_url = f"{self.__jira_repository.base_url}/browse/{issue.key}"
                    "id": "PROJ-1",
                }
            )
        ]
    )

    repository_return_value = (
        PlatformLog(
            loading_items=LoadingItems.JiraIssues,
            timestamp=datetime(2025, 2, 28, 12, 34, 56),
            outcome=True
        ),
        [
            IssueEntity(
                id="10001",
                key="PROJ-1",
                summary="Issue summary",
                description="Detailed description of the issue",
                issuetype={
                    "name": "Bug",
                    "description": "A problem which impairs or prevents the functions of the product."
                },
                project={
                    "id": "10000",
                    "key": "PROJ",
                    "name": "Project Name"
                },
                status={
                    "name": "Open",
                    "description": "The issue is open and ready for the assignee to start work on it."
                },
                priority={
                    "name": "High",
                    "description": "This problem will block progress."
                },
                assignee={
                    "name": "John Doe",
                    "emailAddress": "john.doe@example.com",
                    "displayName": "John Doe"
                },
                reporter={
                    "name": "Jane Smith",
                    "emailAddress": "jane.smith@example.com",
                    "displayName": "Jane Smith"
                },
                created="2025-02-28T12:34:56.000+0000",
                updated="2025-02-28T12:34:56.000+0000",
                attachment=[
                    {
                        "id": "10002",
                        "filename": "example.txt",
                        "content": "https://jira.example.com/secure/attachment/10002/example.txt"
                    }
                ]
            )
        ]
    )

    mock_jira_repository.load_jira_issues.return_value = repository_return_value

    # Act
    result = jira_adapter.load_jira_issues()

    # Assert
    mock_jira_repository.load_jira_issues.assert_called_once()
    assert result == expected_result