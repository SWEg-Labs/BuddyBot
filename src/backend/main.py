import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

from services.githubService import GithubService
from services.jiraService import JiraService
from services.confluenceService import ConfluenceService
from services.vectorStoreService import VectorStoreService
from utils.llm import initialize_llm
from services.chatService import ChatService
from utils.logger import logger

def main():
    try:
        # inizialize language model
        llm = initialize_llm()

        # inizialize vector store
        vector_store = VectorStoreService()

        # create chat service instance
        chat_service = ChatService(llm, vector_store)

        # create the github service instance
        github_service = GithubService()

        # create the jira service instance
        jira_service = JiraService()

        # create the confluence service instance
        confluence_service = ConfluenceService()

        logger.info('Chat initialized. You can:\n' \
                    '- Type a Message\n' \
                    '- Write "exit" to quit\n' \
                    '- Write "help" to see the available commands\n' \
                    '- Write "lg" to load documents from GitHub into the Chroma database \n' \
                    '- Write "lj" to load issues from Jira into the Chroma database \n' \
                    '- Write "lc" to load pages from Confluence into the Chroma database \n' \
                    '- Write "dr" to delete and recreate the Chroma collection \n' \
                    '- Write "v" to view all Chroma documents')

        # Recursive function to keep asking for input
        def ask_question():
            try:
                # Chiede l'input all'utente
                input_text = input("You: ")

                # Controlla il comando di uscita
                if(input_text.lower() == "exit"):
                    logger.info("Exiting the chat application.")
                    return
                elif(input_text.lower() == "help"):
                    logger.info('You can:\n' \
                                '- Type a Message\n' \
                                '- Write "exit" to quit\n' \
                                '- Write "help" to see the available commands\n' \
                                '- Write "lg" to load documents from GitHub into the Chroma database \n' \
                                '- Write "lj" to load issues from Jira into the Chroma database \n' \
                                '- Write "lc" to load pages from Confluence into the Chroma database \n' \
                                '- Write "dr" to delete and recreate the Chroma collection \n' \
                                '- Write "v" to view all Chroma documents')
                elif(input_text.lower() == "lg"):
                    try:
                        # Ottiene i file dal repository GitHub tramite il servizio GitHub
                        repo_files = github_service.get_repository_files(os.getenv("OWNER"), os.getenv("REPO"))

                        for i, file in enumerate(repo_files):
                            logger.info(f"Trying to add document {i}...")
                            vector_store.add_github_documents([file])
                        
                        logger.info(f"Added {len(repo_files)} documents to the vector store.")

                    except Exception as e:
                        logger.error(f"Error getting GitHub files: {e}")
                elif(input_text.lower() == "lj"):
                    try:
                        issues = jira_service.get_issues()

                        for i, issue in enumerate(issues):
                            logger.info(f"Trying to add issue {i}...")
                            vector_store.add_jira_issues([issue])
                        
                        logger.info(f"Added {len(issues)} issues to the vector store.")

                    except Exception as e:
                        logger.error(f"Error getting Jira issues: {e}")
                elif(input_text.lower() == "lc"):
                    try:
                        pages = confluence_service.get_pages()

                        for i, page in enumerate(pages):
                            logger.info(f"Trying to add page {i}...")
                            vector_store.add_confluence_pages([page])
                        
                        logger.info(f"Added {len(pages)} pages to the vector store.")

                    except Exception as e:
                        logger.error(f"Error getting Confluence pages: {e}")
                elif(input_text.lower() == "dr"):
                    try:
                        # Elimina e ricrea la collezione Chroma
                        vector_store.delete_and_recreate_collection()
                        logger.info("The collection has been deleted and recreated successfully.")
                    except Exception as e:
                        logger.error(f"Error removing documents: {e}")
                elif(input_text.lower() == "v"):
                    try:
                        # Visualizza tutti i documenti nel vector store
                        vector_store.view_all_documents()
                    except Exception as e:
                        logger.error(f"Error viewing documents: {e}")
                else:
                    try:
                        # Ottiene la risposta dal servizio LLM
                        response = chat_service.process_user_input(input_text)
                        print("Assistant:", response)
                    except Exception as e:
                        logger.error(f"Error fetching response: {e}")
                
                if input_text.lower() != "help":
                    logger.info("Type 'exit' to quit or 'help' to see the available commands.")


                # Continua la conversazione
                ask_question()
            except KeyboardInterrupt:
                logger.error("\nExiting the chat application.")

        ask_question()
    except Exception as e:
        logger.error(f"Failed to start the chat: {e}")


if __name__ == "__main__":
    main()