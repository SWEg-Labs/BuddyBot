from unittest.mock import MagicMock
from datetime import datetime, timedelta

from models.document import Document
from models.commit_entity import CommitEntity
from models.file_entity import FileEntity
from models.platform_log import PlatformLog
from models.platform import Platform
from adapters.github_adapter import GitHubAdapter
from repositories.github_repository import GitHubRepository


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
                    FileEntity(
                        filename="file1.txt",
                        status="modified",
                        changes=10,
                        additions=5,
                        deletions=5,
                        patch="@@ -1,2 +1,2 @@\n- old line\n+ new line"
                    ),
                    FileEntity(
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
    platform_log = MagicMock()
    document = MagicMock(spec=Document)
    file_entity = MagicMock(spec=FileEntity)
    mock_github_repository.load_github_files.return_value = file_entity

    # Act
    result = github_adapter.load_github_files(platform_log, document)

    # Assert
    mock_github_repository.load_github_files.assert_called_once_with(platform_log, document)
    assert result == file_entity