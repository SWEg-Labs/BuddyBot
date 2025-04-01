import requests
from datetime import datetime
import pytz
from beartype.typing import List, Tuple

from models.loggingModels import PlatformLog, LoadingItems
from entities.issueEntity import IssueEntity
from utils.logger import logger
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
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
        """
        self.__base_url = base_url
        self.__project_key = project_key
        self.__timeout = timeout
        self.__headers = headers

    def get_base_url(self) -> str:
        return self.__base_url

    def load_jira_issues(self) -> Tuple[PlatformLog, List[IssueEntity]]:
        """
        Fetches all issues from the Jira project using pagination.
        Returns:
            Tuple[PlatformLog, List[IssueEntity]]: A tuple containing a log of the operation and a list of issues.
        Raises:
            requests.RequestException: If there is an error during the API request.
        """
        try:
            url = f"{self.__base_url}/rest/api/2/search"
            start_at = 0
            max_results = 100
            issues = []
            total = None  # Il totale delle issues, impostato al primo fetch

            while total is None or start_at < total:
                params = {
                    'jql': f'project={self.__project_key}',
                    'startAt': start_at,
                    'maxResults': max_results
                }

                response = requests.get(url, headers=self.__headers, params=params, timeout=self.__timeout)
                response.raise_for_status()
                data = response.json()

                # Al primo ciclo, impostiamo il totale delle issues presenti in Jira
                if total is None:
                    total = data.get('total', 0)

                issues_data = data.get('issues', [])

                # Converte ogni issue in IssueEntity
                issues.extend([
                    IssueEntity(
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
                    ) for issue in issues_data
                ])

                # logger.info(f"Fetched {len(issues_data)} issues (startAt={start_at}) from Jira project {self.__project_key}") # Per debug

                # Incrementa il valore di start_at per la prossima chiamata
                start_at += max_results

                # Se non sono state ritornate altre issues, interrompiamo il ciclo
                if len(issues_data) < max_results:
                    break

            logger.info(f"Fetched {len(issues)} issues from Jira project {self.__project_key}")
            italy_tz = pytz.timezone('Europe/Rome')
            log = PlatformLog(LoadingItems.JiraIssues, datetime.now(italy_tz), True)

            return log, issues
        except requests.RequestException as e:
            logger.error(f"Error fetching Jira issues: {e}")
            italy_tz = pytz.timezone('Europe/Rome')
            log = PlatformLog(LoadingItems.JiraIssues, datetime.now(italy_tz), False)
            return log, []
        except Exception as e:
            logger.error(f"Error loading Jira issues: {e}")
            raise e
