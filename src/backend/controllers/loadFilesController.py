from utils.logger import logger

class LoadFilesController:
    """
    Controller class to manage file loading operations.
    """
    def __init__(self, vector_store, github_service, jira_service, confluence_service):
        self.vector_store = vector_store
        self.github_service = github_service
        self.jira_service = jira_service
        self.confluence_service = confluence_service

    def load_github_files(self):
        """Loads files from GitHub into the vector store."""
        try:
            repo_files = self.github_service.get_repository_files(os.getenv("OWNER"), os.getenv("REPO"))
            for i, file in enumerate(repo_files):
                logger.info(f"Trying to add file {i}...")
                self.vector_store.add_github_files([file])
            logger.info(f"Added {len(repo_files)} files to the vector store.")
        except Exception as e:
            logger.error(f"Error getting GitHub files: {e}")
            raise e

    def load_github_commits(self):
        """Loads commits from GitHub into the vector store."""
        try:
            commits = self.github_service.get_repository_commits(os.getenv("OWNER"), os.getenv("REPO"))
            for i, commit in enumerate(commits):
                logger.info(f"Trying to add commit {i}...")
                self.vector_store.add_github_commits([commit])
            logger.info(f"Added {len(commits)} commits to the vector store.")
        except Exception as e:
            logger.error(f"Error getting GitHub commits: {e}")
            raise e

    def load_jira(self):
        """Loads issues from Jira into the vector store."""
        try:
            issues = self.jira_service.get_issues()
            for i, issue in enumerate(issues):
                logger.info(f"Trying to add issue {i}...")
                self.vector_store.add_jira_issues([issue])
            logger.info(f"Added {len(issues)} issues to the vector store.")
        except Exception as e:
            logger.error(f"Error getting Jira issues: {e}")
            raise e

    def load_confluence(self):
        """Loads pages from Confluence into the vector store."""
        try:
            pages = self.confluence_service.get_pages()
            for i, page in enumerate(pages):
                logger.info(f"Trying to add page {i}...")
                self.vector_store.add_confluence_pages([page])
            logger.info(f"Added {len(pages)} pages to the vector store.")
        except Exception as e:
            logger.error(f"Error getting Confluence pages: {e}")
            raise e