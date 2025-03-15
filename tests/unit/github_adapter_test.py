import pytest
import unittest.mock
from unittest.mock import MagicMock
from datetime import datetime, timedelta

from models.loggingModels import PlatformLog, LoadingItems
from entities.fileEntity import FileEntity
from adapters.gitHubAdapter import GitHubAdapter
from repositories.gitHubRepository import GitHubRepository


# Verifica che il metodo load_github_commits di GitHubAdapter gestisca correttamente le eccezioni

def test_load_github_commits_exception():
    # Arrange
    mock_github_repository = MagicMock(spec=GitHubRepository)
    github_adapter = GitHubAdapter(mock_github_repository)
    mock_github_repository.load_github_commits.side_effect = Exception("Error while loading commits")

    # Act
    with pytest.raises(Exception) as exc_info:
        github_adapter.load_github_commits()

    # Assert
    assert str(exc_info.value) == "Error while loading commits"


# Verifica che il metodo load_github_files di GitHubAdapter gestisca correttamente le eccezioni

def test_load_github_files_exception():
    # Arrange
    mock_github_repository = MagicMock(spec=GitHubRepository)
    github_adapter = GitHubAdapter(mock_github_repository)
    mock_github_repository.load_github_files.side_effect = Exception("Error while loading files")

    # Act
    with pytest.raises(Exception) as exc_info:
        github_adapter.load_github_files()

    # Assert
    assert str(exc_info.value) == "Error while loading files"


# Verifica che il metodo load_github_files di GitHubAdapter gestisca correttamente le eccezioni di tipo UnicodeDecodeError

def test_load_github_files_unicode_decode_error():
    # Arrange
    mock_github_repository = MagicMock(spec=GitHubRepository)
    github_adapter = GitHubAdapter(mock_github_repository)

    repository_return_value = (
        PlatformLog(
            loading_items=LoadingItems.GitHubFiles,
            timestamp=datetime(2025, 2, 28, 12, 34, 56) - timedelta(minutes=5),
            outcome=True
        ),
        [
            FileEntity(
                type="file",
                encoding="base64",
                size=1234,
                name="example.pdf",
                path="path/to/example.pdf",
                content="JVBERi0xLjQKJcfsj6IKNSAwIG9iago8PC9UeXBlL1BhZ2UvUGFyZW50IDMgMCBSL1Jlc291cmNlcyA2IDAgUi9NZWRpYUJveCBbMCAtMTI3LjggNTkyLjggODQyLjldL0dyb3VwPDwvUy9UcmFuc3BhcmVuY3kvQ1MvRGV2aWNlUkdCL0kgdHJ1ZT4+L0NvbnRlbnRzIDQgMCBSL0Nyb3BCb3ggWy0xMjcuOCAwIDU5Mi44IDg0Mi4xXT4+CmVuZG9iago=",
                sha="abc123",
                url="https://api.github.com/repos/owner/repo/contents/path/to/example.pdf",
                html_url="https://github.com/owner/repo/blob/main/path/to/example.pdf",
                download_url="https://raw.githubusercontent.com/owner/repo/main/path/to/example.pdf",
                git_url="https://api.github.com/repos/owner/repo/git/blobs/abc123"
            )
        ]
    )

    mock_github_repository.load_github_files.return_value = repository_return_value

    # Act
    result = github_adapter.load_github_files()

    # Assert
    mock_github_repository.load_github_files.assert_called_once()
    assert len(result[1]) == 0  # No documents should be returned due to UnicodeDecodeError
