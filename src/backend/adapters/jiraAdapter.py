from typing import List, Tuple

from models.document import Document
from models.loggingModels import PlatformLog
from repositories.jiraRepository import JiraRepository
from utils.logger import logger

class JiraAdapter:
    """
    Adapter class for interacting with Jira issues.
    Attributes:
        jira_repository (JiraRepository): The repository instance for Jira operations.
    """
    def __init__(self, jira_repository: JiraRepository):
        """
        Initializes the JiraAdapter with a JiraRepository instance.
        Args:
            jira_repository (JiraRepository): The repository instance for Jira operations.
        Raises:
            Exception: If an error occurs during initialization.
        """
        try:
            self.jira_repository = jira_repository
        except Exception as e:
            logger.error(f"An error occurred while initializing JiraAdapter: {e}")
            raise

    def load_jira_issues(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Loads Jira issues and adapts them into a list of Document objects.
        Returns:
            Tuple[PlatformLog, List[Document]]: A tuple containing the platform log and a list of adapted documents.
        Raises:
            Exception: If an error occurs while loading or adapting Jira issues.
        """
        try:
            platform_log, issues = self.jira_repository.load_jira_issues()
            documents = [
            Document(
                page_content=issue.summary,
                metadata={
                "project": issue.project["name"],
                "status": issue.status["name"],
                "assignee": issue.assignee["name"],
                "priority": issue.priority["name"],
                "type": issue.issuetype["name"],
                "creation_date": issue.created,
                "url": f"{self.jira_repository.base_url}/browse/{issue.key}",
                "id": issue.key,
                }
            )
            for issue in issues
            ]
            return platform_log, documents
        except Exception as e:
            logger.error(f"An error occurred while adapting Jira issues: {e}")
            return None, []
