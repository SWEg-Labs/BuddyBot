import os
import base64
from github import Github
from utils.logger import logger
from langchain.schema import Document

class GithubService:
    """
    A class that provides methods for interacting with the GitHub API.

    Requires a `GITHUB_TOKEN` environment variable to be set for authentication.

    Raises:
        ValueError: If the `GITHUB_TOKEN` environment variable is not set.
    """
    def __init__(self):
        """
        Initializes the GitHub client using the `GITHUB_TOKEN` environment variable.

        Raises:
            Exception: If an error occurs during initialization
        """
        try:
            github_token = os.getenv("GITHUB_TOKEN")
            if not github_token:
                raise ValueError("GITHUB_TOKEN is not set in the environment variables.")
            
            # Inizializza il client di GitHub
            self.github = Github(github_token)
            logger.info("Initialized Github client")
        except Exception as e:
            logger.error(f"Error initializing Github client: {e}")
            raise

    def get_repositories(self):
        """
        Retrieves a list of open repositories for the authenticated user.

        Returns:
            list: A list of GitHub repository objects.

        Raises:
            Exception: If an error occurs while fetching repositories.
        """
        try:
            # Ottieni una lista di repository per l'utente autenticato
            user = self.github.get_user()
            repositories = user.get_repos()
            return list(repositories)
        except Exception as e:
            logger.error(f"Error fetching repositories: {e}")
            raise

    def get_issues(self, repositories):
        """
        Fetches all open issues from a provided list of GitHub repositories.

        Args:
            repositories (list): A list of GitHub repository objects.

        Returns:
            list: A list of GitHub issue objects.

        Raises:
            Exception: If an error occurs while fetching issues.
        """
        try:
            issues = []
            for repo in repositories:
                repo_issues = repo.get_issues(state="open")
                issues.extend(repo_issues)
            return list(issues)
        except Exception as e:
            logger.error(f"Error fetching issues: {e}")
            raise

    def get_pull_requests(self, repositories):
        """
        Fetches all open pull requests from a provided list of GitHub repositories.

        Args:
            repositories (list): A list of GitHub repository objects.

        Returns:
            list: A list of GitHub pull request objects.

        Raises:
            Exception: If an error occurs while fetching pull requests.
        """
        try:
            pull_requests = []
            for repo in repositories:
                repo_pulls = repo.get_pulls(state="open")
                pull_requests.extend(repo_pulls)
            return list(pull_requests)
        except Exception as e:
            logger.error(f"Error fetching pull requests: {e}")
            raise

    def get_repository_files(self, owner, repo_name):
        """
        Retrieves a list of files from a specified GitHub repository.

        Args:
            owner (str): The owner of the repository.
            repo_name (str): The name of the repository.

        Returns:
            list: A list of `Document` objects containing decoded file content
                  and metadata (type, id, name, path, and URL).

        Raises:
            Exception: If an error occurs while fetching repository files.
        """
        try:
            documents = []
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            contents = repo.get_contents("")  # Root directory
            self._fetch_files_recursively(contents, repo, documents)
            return documents
        except Exception as e:
            logger.error(f"Error fetching repository files: {e}")
            raise

    def _fetch_files_recursively(self, contents, repo, documents):
        """
        Recursively fetches file content and metadata from a GitHub repository.

        This helper function is called internally by `get_repository_files`.

        Args:
            contents (list): A list of GitHub content objects.
            repo (Github.Repository): The GitHub repository object.
            documents (list): A list to store `Document` objects.
        """
        try:
            for content in contents:
                if content.type == "file":
                    file_content = repo.get_contents(content.path)
                    decoded_content = base64.b64decode(file_content.content).decode()
                    documents.append(Document(
                        page_content=decoded_content,
                        metadata={
                            "type": "file",
                            "id": content.sha,
                            "name": content.name,
                            "path": content.path,
                            "url": content.html_url
                        }
                    ))
                elif content.type == "dir":
                    sub_contents = repo.get_contents(content.path)
                    self._fetch_files_recursively(sub_contents, repo, documents)
        except Exception as e:
            logger.error(f"Error fetching repository files recursively: {e}")
            raise
