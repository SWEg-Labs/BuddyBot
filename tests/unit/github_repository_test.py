import pytest
from unittest.mock import MagicMock
from datetime import datetime
from github.Repository import Repository

from models.loggingModels import LoadingItems
from repositories.gitHubRepository import GitHubRepository


# Verifica che il metodo load_github_commits di GitHubRepository carichi correttamente i commit di GitHub

def test_load_github_commits_success():
    # Arrange
    mock_repo = MagicMock(spec=Repository)
    mock_commit = MagicMock()
    mock_commit.sha = "abc123"
    mock_commit.commit.message = "Fix bug in feature X"
    mock_commit.commit.author.name = "John Doe"
    mock_commit.commit.author.email = "john.doe@example.com"
    mock_commit.commit.author.date = datetime(2025, 2, 28, 12, 34, 56)
    mock_commit.html_url = "https://github.com/owner/repo/commit/abc123"
    mock_commit.files = [
        MagicMock(filename="file1.txt", status="modified", changes=10, additions=5, deletions=5, patch="@@ -1,2 +1,2 @@\n- old line\n+ new line"),
        MagicMock(filename="file2.txt", status="added", changes=20, additions=20, deletions=0, patch="@@ -0,0 +1,20 @@\n+ new content")
    ]
    mock_repo.get_commits.return_value = [mock_commit]
    github_repository = GitHubRepository(mock_repo)

    # Act
    log, commits = github_repository.load_github_commits()

    # Assert
    assert log.get_loading_items() == LoadingItems.GitHubCommits
    assert log.get_outcome() is True
    assert len(commits) == 1
    assert commits[0].get_sha() == "abc123"
    assert commits[0].get_message() == "Fix bug in feature X"


# Verifica che il metodo load_github_commits di GitHubRepository gestisca correttamente le eccezioni

def test_load_github_commits_exception():
    # Arrange
    mock_repo = MagicMock(spec=Repository)
    mock_repo.get_commits.side_effect = Exception("Error fetching commits")
    github_repository = GitHubRepository(mock_repo)

    # Act
    log, commits = github_repository.load_github_commits()

    # Assert
    assert log.get_loading_items() == LoadingItems.GitHubCommits
    assert log.get_outcome() is False
    assert commits == []


# Verifica che il metodo load_github_files di GitHubRepository carichi correttamente i file di GitHub

def test_load_github_files_success():
    # Arrange
    mock_repo = MagicMock(spec=Repository)
    mock_file = MagicMock()
    mock_file.type = "file"
    mock_file.encoding = "base64"
    mock_file.size = 1234
    mock_file.name = "example.txt"
    mock_file.path = "path/to/example.txt"
    mock_file.content = "SGVsbG8gd29ybGQhCg=="
    mock_file.sha = "abc123"
    mock_file.url = "https://api.github.com/repos/owner/repo/contents/path/to/example.txt"
    mock_file.html_url = "https://github.com/owner/repo/blob/main/path/to/example.txt"
    mock_file.download_url = "https://raw.githubusercontent.com/owner/repo/main/path/to/example.txt"
    mock_file.git_url = "https://api.github.com/repos/owner/repo/git/blobs/abc123"
    mock_repo.get_contents.return_value = [mock_file]
    github_repository = GitHubRepository(mock_repo)

    # Act
    log, files = github_repository.load_github_files()

    # Assert
    assert log.get_loading_items() == LoadingItems.GitHubFiles
    assert log.get_outcome() is True
    assert len(files) == 1
    assert files[0].get_name() == "example.txt"
    assert files[0].get_content() == "SGVsbG8gd29ybGQhCg=="


# Verifica che il metodo load_github_files di GitHubRepository gestisca correttamente le eccezioni

def test_load_github_files_exception():
    # Arrange
    mock_repo = MagicMock(spec=Repository)
    mock_repo.get_contents.side_effect = Exception("Error fetching files")
    github_repository = GitHubRepository(mock_repo)

    # Act
    log, files = github_repository.load_github_files()

    # Assert
    assert log.get_loading_items() == LoadingItems.GitHubFiles
    assert log.get_outcome() is False
    assert files == []


# Verifica che il metodo load_github_files di GitHubRepository gestisca correttamente le directory

def test_load_github_files_with_directory():
    # Arrange
    mock_repo = MagicMock(spec=Repository)
    mock_dir = MagicMock()
    mock_dir.type = "dir"
    mock_dir.path = "path/to/dir"
    mock_file_in_dir = MagicMock()
    mock_file_in_dir.type = "file"
    mock_file_in_dir.encoding = "base64"
    mock_file_in_dir.size = 1234
    mock_file_in_dir.name = "example_in_dir.txt"
    mock_file_in_dir.path = "path/to/dir/example_in_dir.txt"
    mock_file_in_dir.content = "SGVsbG8gd29ybGQhCg=="
    mock_file_in_dir.sha = "abc123"
    mock_file_in_dir.url = "https://api.github.com/repos/owner/repo/contents/path/to/dir/example_in_dir.txt"
    mock_file_in_dir.html_url = "https://github.com/owner/repo/blob/main/path/to/dir/example_in_dir.txt"
    mock_file_in_dir.download_url = "https://raw.githubusercontent.com/owner/repo/main/path/to/dir/example_in_dir.txt"
    mock_file_in_dir.git_url = "https://api.github.com/repos/owner/repo/git/blobs/abc123"
    mock_repo.get_contents.side_effect = [[mock_dir], [mock_file_in_dir]]
    github_repository = GitHubRepository(mock_repo)

    # Act
    log, files = github_repository.load_github_files()

    # Assert
    assert log.get_loading_items() == LoadingItems.GitHubFiles
    assert log.get_outcome() is True
    assert len(files) == 1
    assert files[0].get_name() == "example_in_dir.txt"
    assert files[0].get_content() == "SGVsbG8gd29ybGQhCg=="

