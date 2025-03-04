from github.Repository import Repository
from datetime import datetime
import pytz
from typing import Tuple, List

from models.loggingModels import PlatformLog, LoadingItems
from entities.commitEntity import CommitEntity, CommitFileEntity
from entities.fileEntity import FileEntity
from utils.logger import logger

class GitHubRepository:
    """
    A repository class to interact with a GitHub repository using the provided GitHub API.
    Attributes:
        github_repo (Repository): The GitHub repository object.
    """

    def __init__(self, github_repo: Repository):
        """
        Initializes the GitHubRepository with a given GitHub repository object.
        Args:
            github_repo (Repository): The GitHub repository object.
        Raises:
            Exception: If there is an error initializing the GitHubRepository.
        """
        try:
            self.__github_repo = github_repo
        except Exception as e:
            logger.error(f"Error initializing GitHubRepository: {e}")
            raise

    def load_github_commits(self) -> Tuple[PlatformLog, List[CommitEntity]]:
        """
        Loads the commits from the GitHub repository.
        Returns:
            tuple: A tuple containing a PlatformLog object and a list of CommitEntity objects.
        Raises:
            Exception: If there is an error fetching commits for the repository.
        """
        try:
            commits = self.__github_repo.get_commits()
            commit_entities = []

            for commit in commits:
                files = [CommitFileEntity(f.filename, f.status, f.changes, f.additions, f.deletions, f.patch) for f in commit.files]
                commit_entity = CommitEntity(commit.sha, commit.commit.message, commit.commit.author.name, commit.commit.author.email, commit.commit.author.date, commit.html_url, files)
                commit_entities.append(commit_entity)

            logger.info(f"Fetched {len(commit_entities)} commits for repository {self.__github_repo.full_name}")
            italy_tz = pytz.timezone('Europe/Rome')
            log = PlatformLog(LoadingItems.GitHubCommits, datetime.now(italy_tz), True)

            return log, commit_entities
        except Exception as e:
            logger.error(f"Error fetching commits for repository {self.__github_repo.full_name}: {e}")
            log = PlatformLog(LoadingItems.GitHubCommits, datetime.now(italy_tz), False)
            return log, []

    def load_github_files(self) -> Tuple[PlatformLog, List[FileEntity]]:
        """
        Loads the files from the GitHub repository.
        Returns:
            tuple: A tuple containing a PlatformLog object and a list of FileEntity objects.
        Raises:
            Exception: If there is an error fetching files for the repository.
        """
        try:
            contents = self.__github_repo.get_contents("")
            file_entities = []

            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(self.__github_repo.get_contents(file_content.path))
                else:
                    file_entity = FileEntity(file_content.type, file_content.encoding, file_content.size, file_content.name, file_content.path, file_content.content, file_content.sha, file_content.url, file_content.html_url, file_content.download_url, file_content.git_url)
                    file_entities.append(file_entity)

            logger.info(f"Fetched {len(file_entities)} files for repository {self.__github_repo.full_name}")
            italy_tz = pytz.timezone('Europe/Rome')
            log = PlatformLog(LoadingItems.GitHubFiles, datetime.now(italy_tz), True)

            return log, file_entities
        except Exception as e:
            logger.error(f"Error fetching files for repository {self.__github_repo.full_name}: {e}")
            log = PlatformLog(LoadingItems.GitHubFiles, datetime.now(italy_tz), False)
            return log, []
