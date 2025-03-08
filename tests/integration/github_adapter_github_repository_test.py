from unittest.mock import MagicMock
from datetime import datetime, timedelta

from models.document import Document
from models.loggingModels import PlatformLog, LoadingItems
from entities.commitEntity import CommitEntity, CommitFileEntity
from entities.fileEntity import FileEntity
from adapters.gitHubAdapter import GitHubAdapter
from repositories.gitHubRepository import GitHubRepository


# Verifica che il metodo load_github_commits di GitHubAdapter chiami il metodo load_github_commits di GitHubtRepository

def test_load_github_commits_calls_repository_method():
    # Arrange
    mock_github_repository = MagicMock(spec=GitHubRepository)
    github_adapter = GitHubAdapter(mock_github_repository)

    expected_result = (
        PlatformLog(
            loading_items=LoadingItems.GitHubCommits,
            timestamp=datetime(2025, 2, 28, 12, 34, 56) - timedelta(minutes=5),
            outcome=True
        ),
        [
            Document(
                page_content="Fix bug in feature X",
                metadata={
                    "author": "John Doe",
                    "email": "john.doe@example.com",
                    "date": "2025-02-28T12:34:56Z",
                    "files": [
                        "- file1.txt (Status: modified, Changes: 10, Additions: 5, Deletions: 5)\n  Patch:\n@@ -1,2 +1,2 @@\n- old line\n+ new line",
                        "- file2.txt (Status: added, Changes: 20, Additions: 20, Deletions: 0)\n  Patch:\n@@ -0,0 +1,20 @@\n+ new content"
                    ],
                    "item_type": "GitHub Commit",
                    "url": "https://github.com/owner/repo/commit/abc123",
                    "id": "abc123",
                }
            )
        ]
    )

    repository_return_value = (
        PlatformLog(
            loading_items=LoadingItems.GitHubCommits,
            timestamp=datetime(2025, 2, 28, 12, 34, 56) - timedelta(minutes=5),
            outcome=True
        ),
        [
            CommitEntity(
                sha="abc123",
                message="Fix bug in feature X",
                author_name="John Doe",
                author_email="john.doe@example.com",
                author_date="2025-02-28T12:34:56Z",
                url="https://github.com/owner/repo/commit/abc123",
                files=[
                    CommitFileEntity(
                        filename="file1.txt",
                        status="modified",
                        changes=10,
                        additions=5,
                        deletions=5,
                        patch="@@ -1,2 +1,2 @@\n- old line\n+ new line"
                    ),
                    CommitFileEntity(
                        filename="file2.txt",
                        status="added",
                        changes=20,
                        additions=20,
                        deletions=0,
                        patch="@@ -0,0 +1,20 @@\n+ new content"
                    )
                ]
            )
        ]
    )

    mock_github_repository.load_github_commits.return_value = repository_return_value

    # Act
    result = github_adapter.load_github_commits()

    # Assert
    mock_github_repository.load_github_commits.assert_called_once()
    assert result == expected_result


# Verifica che il metodo load_github_files di GitHubAdapter chiami il metodo load_github_files di GitHubtRepository

def test_load_github_files_calls_repository_method():
    # Arrange
    mock_github_repository = MagicMock(spec=GitHubRepository)
    github_adapter = GitHubAdapter(mock_github_repository)

    expected_result = (
        PlatformLog(
            loading_items=LoadingItems.GitHubFiles,
            timestamp=datetime(2025, 2, 28, 12, 34, 56) - timedelta(minutes=5),
            outcome=True
        ),
        [
            Document(
                page_content="Hello world!\n",  # Contenuto decodificato dalla codifica base64
                metadata={
                    "type": "file",
                    "name": "example.txt",
                    "path": "path/to/example.txt",
                    "item_type": "GitHub File",
                    "url": "https://github.com/owner/repo/blob/main/path/to/example.txt", # html_url
                    "id": "abc123",
                }
            )
        ]
    )

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
                name="example.txt",
                path="path/to/example.txt",
                content="SGVsbG8gd29ybGQhCg==", # Contenuto codificato, decodificato è "Hello world!\n"
                sha="abc123",
                url="https://api.github.com/repos/owner/repo/contents/path/to/example.txt",
                html_url="https://github.com/owner/repo/blob/main/path/to/example.txt",
                download_url="https://raw.githubusercontent.com/owner/repo/main/path/to/example.txt",
                git_url="https://api.github.com/repos/owner/repo/git/blobs/abc123"
            )
        ]
    )

    mock_github_repository.load_github_files.return_value = repository_return_value

    # Act
    result = github_adapter.load_github_files()

    # Assert
    mock_github_repository.load_github_files.assert_called_once()
    assert result == expected_result
