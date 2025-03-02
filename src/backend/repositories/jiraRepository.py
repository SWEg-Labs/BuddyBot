import requests
from datetime import datetime
from typing import List, Tuple

from models.loggingModels import PlatformLog, LoadingItems
from entities.issueEntity import IssueEntity
from utils.logger import logger

class JiraRepository:
    """
    A repository class for interacting with Jira API to fetch issues.
    Attributes:
        base_url (str): The base URL of the Jira instance.
        project_key (str): The key of the Jira project.
        timeout (int): The timeout for API requests.
        headers (dict[str, str]): The headers to include in API requests.
    """

    def __init__(self, base_url: str, project_key: str, timeout: int, headers: dict[str, str]):
        """
        Initializes the JiraRepository with the given parameters.
        Args:
            base_url (str): The base URL of the Jira instance.
            project_key (str): The key of the Jira project.
            timeout (int): The timeout for API requests.
            headers (dict[str, str]): The headers to include in API requests.
        Raises:
            Exception: If there is an error during initialization.
        """
        try:
            self.__base_url = base_url
            self.__project_key = project_key
            self.__timeout = timeout
            self.__headers = headers
        except Exception as e:
            logger.error(f"Error initializing JiraRepository: {e}")
            raise

    def get_base_url(self):
        return self.__base_url

    def get_project_key(self):
        return self.__project_key

    def get_timeout(self):
        return self.__timeout

    def get_headers(self):
        return self.__headers

    def load_jira_issues(self) -> Tuple[PlatformLog, List[IssueEntity]]:
        """
        Fetches issues from the Jira project.
        Returns:
            Tuple[PlatformLog, List[IssueEntity]]: A tuple containing a log of the operation and a list of issues.
        Raises:
            requests.RequestException: If there is an error during the API request.
        """
        try:
            url = f"{self.__base_url}/rest/api/2/search"
            params = {
                'jql': f'project={self.__project_key}',
                "maxResults": 50
            }

            response = requests.get(url, headers=self.__headers, params=params, timeout=self.__timeout)
            response.raise_for_status()
            issues_data = response.json().get('issues', [])

            issues = [IssueEntity(
                id=issue['id'],
                key=issue['key'],
                summary=issue['fields']['summary'],
                description=issue['fields'].get('description', ''),
                issuetype=issue['fields']['issuetype'],
                project=issue['fields']['project'],
                status=issue['fields']['status'],
                priority=issue['fields'].get('priority', {}),
                assignee=issue['fields'].get('assignee', {}),
                reporter=issue['fields'].get('reporter', {}),
                created=issue['fields']['created'],
                updated=issue['fields']['updated'],
                attachment=issue['fields'].get('attachment', [])
            ) for issue in issues_data]

            logger.info(f"Fetched {len(issues)} issues from Jira project {self.__project_key}")
            log = PlatformLog(LoadingItems.JiraIssues, datetime.now(), True)

            return log, issues
        except requests.RequestException as e:
            logger.error(f"Error fetching Jira issues: {e}")
            log = PlatformLog(LoadingItems.JiraIssues, datetime.now(), False)
            return log, []
