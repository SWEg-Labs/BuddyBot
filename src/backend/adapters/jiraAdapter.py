from beartype.typing import List, Tuple

from models.document import Document
from models.loggingModels import PlatformLog
from ports.jiraPort import JiraPort
from repositories.jiraRepository import JiraRepository
from utils.logger import logger
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
class JiraAdapter(JiraPort):
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
        """
        self.__jira_repository = jira_repository

    def load_jira_issues(self) -> Tuple[PlatformLog, List[Document]]:
        """
        Loads Jira issues and adapts them into a list of Document objects.
        Returns:
            Tuple[PlatformLog, List[Document]]: A tuple containing the platform log and a list of adapted documents.
        Raises:
            Exception: If an error occurs while loading or adapting Jira issues.
        """
        try:
            platform_log, issue_entities = self.__jira_repository.load_jira_issues()

            documents = [
                Document(
                    page_content=issue.get_summary() if issue.get_summary() is not None else "/",
                    metadata={
                        "project": issue.get_project().get("name")
                                   if issue.get_project() and issue.get_project().get("name") is not None else "/",
                        "status": issue.get_status().get("name")
                                  if issue.get_status() and issue.get_status().get("name") is not None else "/",
                        "assignee": issue.get_assignee().get("displayName")
                                    if issue.get_assignee() and issue.get_assignee().get("displayName") is not None else "/",
                        "priority": issue.get_priority().get("name")
                                    if issue.get_priority() and issue.get_priority().get("name") is not None else "/",
                        "type": issue.get_issuetype().get("name")
                                if issue.get_issuetype() and issue.get_issuetype().get("name") is not None else "/",
                        "item_type": "Jira Issue",
                        "creation_date": issue.get_created()
                                        if issue.get_created() is not None else "/",
                        "url": (f"{self.__jira_repository.get_base_url()}/browse/{issue.get_key()}"
                                if self.__jira_repository.get_base_url() is not None and issue.get_key() is not None else "/"),
                        "id": issue.get_key()
                              if issue.get_key() is not None else "/",
                        "last_update": issue.get_updated()
                                if issue.get_updated() is not None else "/",
                    }
                )
                for issue in issue_entities
            ]
            return platform_log, documents
        except Exception as e:
            logger.error(f"An error occurred while adapting Jira issues: {e}")
            raise e
