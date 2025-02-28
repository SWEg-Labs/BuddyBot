from unittest.mock import MagicMock
from datetime import datetime, timedelta

from models.document import Document
from models.platformLog import PlatformLog
from models.platform import Platform
from entities.commitEntity import CommitEntity
from entities.commitFileEntity import CommitFileEntity
from entities.fileEntity import FileEntity
from adapters.githubAdapter import GitHubAdapter
from repositories.githubRepository import GitHubRepository


# Verifica che il metodo load_github_commits di GitHubAdapter chiami il metodo load_github_commits di GitHubtRepository

def test_load_github_commits_calls_repository_method():
    # Arrange
    mock_github_repository = MagicMock(spec=GitHubRepository)
    github_adapter = GitHubAdapter(mock_github_repository)

    expected_result = (
        PlatformLog(
            platform=Platform.GitHub,
            timestamp=datetime.now() - timedelta(minutes=5),
            outcome=True
        ),
        [
            Document(
                page_content="Fix bug in feature X",
                metadata={
                    "author": "John Doe",
                    "email": "john.doe@example.com",
                    "date": "2025-02-28T12:34:56Z",
                    "commit_hash": "abc123",
                    "url": "https://github.com/owner/repo/commit/abc123",
                    "files": [
                        "- file1.txt (Status: modified, Changes: 10, Additions: 5, Deletions: 5)\n  Patch:\n@@ -1,2 +1,2 @@\n- old line\n+ new line\n",
                        "- file2.txt (Status: added, Changes: 20, Additions: 20, Deletions: 0)\n  Patch:\n@@ -0,0 +1,20 @@\n+ new content\n"
                    ],
                    "chunk_index": 0,
                    "doc_id": "abc123_0"
                }
            )
        ]
    )

    repository_return_value = (
        PlatformLog(
            platform=Platform.GitHub,
            timestamp=datetime.now() - timedelta(minutes=5),
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
            platform=Platform.GitHub,
            timestamp=datetime.now() - timedelta(minutes=5),
            outcome=True
        ),
        [
            Document(
                page_content="Hello world!\n",  # Contenuto decodificato dalla codifica base64
                metadata={
                    "type": "file",
                    "id": "abc123",
                    "name": "example.txt",
                    "path": "path/to/example.txt",
                    "url": "https://github.com/owner/repo/blob/main/path/to/example.txt",
                    "chunk_index": 0,
                    "doc_id": "abc123_0"
                }
            )
        ]
    )

    repository_return_value = (
        PlatformLog(
            platform=Platform.GitHub,
            timestamp=datetime.now() - timedelta(minutes=5),
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

    mock_github_repository.load_github_commits.return_value = repository_return_value

    # Act
    result = github_adapter.load_github_files()

    # Assert
    mock_github_repository.load_github_files.assert_called_once()
    assert result == expected_result
