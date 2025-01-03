import os
from utils.logger import logger

class UserController:
    """
    Controller class to manage user interactions in the chat application.

    This class contains methods for handling user input and processing commands.
    """

    @staticmethod
    def ask_question(vector_store, chat_service, github_service, jira_service, confluence_service):
        """
        Static method to ask the user for input and process it.

        Args:
            vector_store (VectorStoreRepository): Instance of the vector store repository.
            chat_service (ChatService): Instance of the chat service.
            github_service (GithubService): Instance of the GitHub service.
            jira_service (JiraService): Instance of the Jira service.
            confluence_service (ConfluenceService): Instance of the Confluence service.

        Raises:
            KeyboardInterrupt: If the user exits the chat application.
        """
        try:
            input_text = input("You: ")
            UserController._handle_command(
                input_text, vector_store, chat_service,
                github_service, jira_service, confluence_service
            )

            # Continua a chiedere finché non viene digitato "exit"
            UserController.ask_question(vector_store, chat_service, github_service, jira_service, confluence_service)
        except KeyboardInterrupt:
            logger.error("\nExiting the chat application.")

    @staticmethod
    def _handle_command(input_text, vector_store, chat_service, github_service, jira_service, confluence_service):
        """
        Processes a user command.

        Args:
            input_text (str): The command input by the user.
            vector_store (VectorStoreRepository): Instance of the vector store repository.
            chat_service (ChatService): Instance of the chat service.
            github_service (GithubService): Instance of the GitHub service.
            jira_service (JiraService): Instance of the Jira service.
            confluence_service (ConfluenceService): Instance of the Confluence service.
        """
        command_handlers = {
            "exit": UserController._exit_application,
            "help": UserController._show_help,
            "lgf": UserController._load_github_files,
            "lgc": UserController._load_github_commits,
            "lj": UserController._load_jira,
            "lc": UserController._load_confluence,
            "dr": UserController._delete_and_recreate,
            "v": UserController._view_documents,
        }

        if input_text.lower() in command_handlers:  # case insensitive
            command_handlers[input_text.lower()](vector_store, github_service, jira_service, confluence_service)
        else:
            UserController._process_chat(input_text, chat_service)

        if input_text.lower() != "help":
            print()   # Print a new line after each command
            logger.info("Type a message! Otherwise, you can type 'exit' to quit or 'help' to see the available commands.")

    @staticmethod
    def _exit_application(*args):
        """Exits the chat application."""
        logger.info("Exiting the chat application.")
        exit()

    @staticmethod
    def _show_help(*args):
        """Displays help commands to the user."""
        logger.info('You can:\n'
                    '- Type a Message\n'
                    '- Write "exit" to quit\n'
                    '- Write "help" to see the available commands\n'
                    '- Write "lgf" to load files from GitHub into the Chroma database\n'
                    '- Write "lgc" to load commits from GitHub into the Chroma database\n'
                    '- Write "lj" to load issues from Jira into the Chroma database\n'
                    '- Write "lc" to load pages from Confluence into the Chroma database\n'
                    '- Write "dr" to delete and recreate the Chroma collection\n'
                    '- Write "v" to view all Chroma documents')

    @staticmethod
    def _load_github_files(vector_store, github_service, *args):
        """Loads files from GitHub into the vector store."""
        try:
            repo_files = github_service.get_repository_files(os.getenv("OWNER"), os.getenv("REPO"))
            for i, file in enumerate(repo_files):
                logger.info(f"Trying to add file {i}...")
                vector_store.add_github_files([file])
            logger.info(f"Added {len(repo_files)} files to the vector store.")
        except Exception as e:
            logger.error(f"Error getting GitHub files: {e}")

    @staticmethod
    def _load_github_commits(vector_store, github_service, *args):
        """Loads commits from GitHub into the vector store."""
        try:
            commits = github_service.get_repository_commits(os.getenv("OWNER"), os.getenv("REPO"))

            for i, commit in enumerate(commits):
                logger.info(f"Trying to add commit {i}...")
                vector_store.add_github_commits([commit])
            logger.info(f"Added {len(commits)} commits to the vector store.")
        except Exception as e:
            logger.error(f"Error getting GitHub commits: {e}")

    @staticmethod
    def _load_jira(vector_store, *args):
        """Loads issues from Jira into the vector store."""
        try:
            issues = args[1].get_issues()
            for i, issue in enumerate(issues):
                logger.info(f"Trying to add issue {i}...")
                vector_store.add_jira_issues([issue])
            logger.info(f"Added {len(issues)} issues to the vector store.")
        except Exception as e:
            logger.error(f"Error getting Jira issues: {e}")

    @staticmethod
    def _load_confluence(vector_store, *args):
        """Loads pages from Confluence into the vector store."""
        try:
            pages = args[2].get_pages()
            for i, page in enumerate(pages):
                logger.info(f"Trying to add page {i}...")
                vector_store.add_confluence_pages([page])
            logger.info(f"Added {len(pages)} pages to the vector store.")
        except Exception as e:
            logger.error(f"Error getting Confluence pages: {e}")

    @staticmethod
    def _delete_and_recreate(vector_store, *args):
        """Deletes and recreates the vector store collection."""
        try:
            vector_store.delete_and_recreate_collection()
            logger.info("The collection has been deleted and recreated successfully.")
        except Exception as e:
            logger.error(f"Error removing documents: {e}")

    @staticmethod
    def _view_documents(vector_store, *args):
        """Views all documents in the vector store."""
        try:
            vector_store.view_all_documents()
        except Exception as e:
            logger.error(f"Error viewing documents: {e}")

    @staticmethod
    def _process_chat(input_text, chat_service):
        """Processes user input and fetches a response from the chat service."""
        try:
            response = chat_service.process_user_input(input_text)
            print("\n\nAssistant:\n", response)
        except Exception as e:
            logger.error(f"Error fetching response: {e}")
