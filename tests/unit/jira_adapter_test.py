import pytest
from unittest.mock import MagicMock
from adapters.jiraAdapter import JiraAdapter
from repositories.jiraRepository import JiraRepository


# Verifica che il metodo load_jira_issues di JiraAdapter gestisca correttamente le eccezioni

def test_load_jira_issues_exception_handling():
    # Arrange
    mock_jira_repository = MagicMock(spec=JiraRepository)
    jira_adapter = JiraAdapter(mock_jira_repository)

    mock_jira_repository.load_jira_issues.side_effect = Exception("Loading Jira issues error")

    # Act
    with pytest.raises(Exception) as exc_info:
        jira_adapter.load_jira_issues()

    # Assert
    assert str(exc_info.value) == "Loading Jira issues error"
