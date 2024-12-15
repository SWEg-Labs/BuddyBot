import os
import requests
import base64
from utils.logger import logger
from langchain.schema import Document

class JiraService:
    """
    A class that provides methods for interacting with the Jira API.

    Requires
    - `ATLASSIAN_TOKEN` and `ATLASSIAN_USER_EMAIL` environment variables for authentication.
    - `JIRA_BASE_URL` and `JIRA_PROJECT_KEY` environment variables for configuration.

    Raises:
        ValueError: If any of the required environment variables are missing.
    """
    def __init__(self):
        """
        Initializes the Jira client using the required environment variables.

        Raises:
            Exception: If an error occurs during initialization.
        """
        try:
            self.token = os.getenv("ATLASSIAN_TOKEN")
            self.email = os.getenv("ATLASSIAN_USER_EMAIL")
            self.base_url = os.getenv("JIRA_BASE_URL")
            self.project_key = os.getenv("JIRA_PROJECT_KEY")
            self.timeout = int(os.getenv("TIMEOUT", "10"))

            if not all([self.token, self.email, self.base_url, self.project_key]):
                raise ValueError("Environment variables ATLASSIAN_TOKEN, ATLASSIAN_USER_EMAIL, JIRA_BASE_URL, or JIRA_PROJECT_KEY are missing.")
            
        # Codifica in Base64
            auth_str = f"{self.email}:{self.token}"
            auth_bytes = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

            self.headers = {
                "Authorization": f"Basic {auth_bytes}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            logger.info("Initialized Jira client")
        except Exception as e:
            logger.error(f"Error initializing Jira client: {e}")
            raise

    def get_projects(self):
        """
        Fetches a list of projects from Jira.

        Returns:
            list: A list of Jira project objects.

        Raises:
            Exception: If an error occurs while fetching projects.
        """
        try:
            url = f"{self.base_url}/rest/api/3/project"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            projects = response.json()
            return projects
        except Exception as e:
            logger.error(f"Error fetching projects: {e}")
            raise

    def get_issues(self):
        """
        Fetches all open issues from the configured Jira project.

        Returns:
            list: A list of Jira issue objects.

        Raises:
            Exception: If an error occurs while fetching issues.
        """
        try:
            url = f"{self.base_url}/rest/api/3/search"
            params = {
                "jql": f"project={self.project_key} AND status!=Done",
                "maxResults": 50
            }
            response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            issues = response.json().get("issues", [])
            return issues
        except Exception as e:
            logger.error(f"Error fetching issues: {e}")
            raise

    def get_issue_details(self, issue_key):
        """
        Fetches the details of a specific Jira issue.

        Args:
            issue_key (str): The key of the Jira issue.

        Returns:
            dict: A dictionary containing the details of the Jira issue.

        Raises:
            Exception: If an error occurs while fetching issue details.
        """
        try:
            url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching issue details for {issue_key}: {e}")
            raise

    def get_issue_attachments(self):
        """
        Fetches all attachments from the open issues in the configured Jira project.

        Returns:
            list: A list of Document objects representing the attachments.

        Raises:
            Exception: If an error occurs while fetching attachments.
        """
        try:
            issues = self.get_issues()
            documents = []
            for issue in issues:
                if "fields" in issue and "attachment" in issue["fields"]:
                    for attachment in issue["fields"]["attachment"]:
                        file_url = attachment["content"]
                        response = requests.get(file_url, headers=self.headers, timeout=self.timeout)
                        response.raise_for_status()
                        documents.append(Document(
                            page_content=response.text,
                            metadata={
                                "type": "attachment",
                                "name": attachment["filename"],
                                "url": attachment["content"],
                                "issue_key": issue["key"]
                            }
                        ))
            return documents
        except Exception as e:
            logger.error(f"Error fetching project files: {e}")
            raise
