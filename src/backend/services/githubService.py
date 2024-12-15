import os
import base64
from github import Github
from utils.logger import logger
from langchain.schema import Document

class GithubService:
    def __init__(self):
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
        try:
            # Ottieni una lista di repository per l'utente autenticato
            user = self.github.get_user()
            repositories = user.get_repos()
            return list(repositories)
        except Exception as e:
            logger.error(f"Error fetching repositories: {e}")
            raise

    def get_issues(self, repositories):
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
