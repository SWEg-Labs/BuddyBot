import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import openai
from langchain_core.documents import Document
from utils.logger import logger

class VectorStoreService:
    def __init__(self):
        self.client = None
        self.collection_name = None
        self.collection = None
        self.initialize_vector_store()

    def initialize_vector_store(self):
        # Connetti al server ChromaDB
        self.client = chromadb.HttpClient(host="localhost", port=8000)
        self.client.heartbeat()  # Verifica connessione

        self.collection_name = "buddybot-vector-store"

        # Crea o ottieni una collezione esistente
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
        )
        logger.info("Successfully connected to Chroma vector store.")

    def split_github_documents(self, documents):
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            split_docs = text_splitter.create_documents([doc.page_content for doc in documents])
            logger.info(f"Documents split into {len(split_docs)} chunks.")
            return split_docs
        except Exception as error:
            logger.error(f"Error splitting documents: {error}")
            raise

    def add_github_documents(self, documents):
        try:
            # split_docs = self.split_documents(documents)
            # for doc in split_docs:
            for doc in documents:
                self.collection.add(
                    documents=[doc.page_content],
                    metadatas=[doc.metadata],
                    ids=[doc.metadata["id"]],
                )
            logger.info("Documents added successfully to vector store.")
        except Exception as error:
            logger.error(f"Error adding documents to vector store: {error}")
            raise

    def add_jira_issues(self, issues):
        """
        Adds a list of issues to the Chroma database.

        Args:
            issues (list): A list of dictionaries representing issues. Each dictionary
                        should contain the following keys:
                            - summary (str): The summary of the issue.
                            - project (str): The project the issue belongs to.
                            - status (str): The current status of the issue.
                            - assignee (str, optional): The assignee of the issue.
                            - priority (str, optional): The priority of the issue.
                            - id (str, optional): The unique identifier of the issue.

        Returns:
            None

        Raises:
            Exception: If an error occurs while adding the issues to Chroma.
        """

        try:
            for issue in issues:
                assignee = issue["fields"].get("assignee")
                if assignee:
                    assignee_name = assignee["displayName"]
                else:
                    assignee_name = "" # Default to empty string if assignee is not present (NoneType)

                # Extract issue data based on Chroma's expected format
                document = {
                    "page_content": issue["fields"]["summary"],
                    "metadatas": {
                        "project": issue["fields"]["project"]["name"],
                        "status": issue["fields"]["status"]["name"],
                        "assignee": assignee_name,
                        "priority": issue["fields"]["priority"]["name"],
                        "id": issue["key"],
                    },
                }

                self.collection.add(
                    documents=[document["page_content"]],
                    metadatas=[document["metadatas"]],
                    ids=[document["metadatas"]["id"]],
                )

            logger.info("Issues added successfully to Chroma database.")
        except Exception as error:
            logger.error(f"Error adding issues to Chroma database: {error}")
            raise

    def add_confluence_pages(self, pages):
        """
        Adds a list of Confluence pages to the Chroma database.

        Args:
            pages (list): A list of dictionaries representing Confluence pages.
                Each dictionary should contain the following keys:
                    - id (str): The unique identifier of the page.
                    - title (str): The title of the Confluence page.
                    - body (str): The content of the page body.
                    - version (dict, optional): Information about the version of the page.

        Returns:
            None

        Raises:
            Exception: If an error occurs while adding the pages to Chroma.
        """

        try:
            for page in pages:
                # Extract relevant data from the Confluence page
                page_title = page["title"]
                page_content = page["body"]["storage"]["value"]

                # Prepare document structure for Chroma
                document = {
                    "page_content": page_content,
                    "metadatas": {
                        "title": page_title,  # Add title as metadata
                        "page_id": page["id"],  # Include page ID for potential reference
                    }
                }

                # Add version information if available (optional)
                if page.get("version"):
                    version_info = page["version"]
                    document["metadatas"]["created_by"] = version_info.get("createdBy", {}).get("displayName", "")
                    document["metadatas"]["created_date"] = version_info.get("created", "")

                # Add the page to Chroma
                self.collection.add(
                    documents=[document["page_content"]],
                    metadatas=[document["metadatas"]],
                    ids=[page["id"]],  # Use page ID as unique identifier
                )

            logger.info("Confluence pages added successfully to Chroma database.")
        except Exception as error:
            logger.error(f"Error adding Confluence pages to Chroma database: {error}")
            raise

    def view_all_documents(self):
        try:
            # Recupera tutti i documenti nella collezione
            all_documents = self.collection.get()
            
            # Itera sui documenti e stampa i dettagli
            for doc_id, doc_content, doc_metadata in zip(
                all_documents["ids"], 
                all_documents["documents"], 
                all_documents["metadatas"]
            ):
                print(f"Document ID: {doc_id}")
                print(f"Content: {doc_content}")
                print(f"Metadata: {doc_metadata}")
                print("-" * 50)
            
            logger.info(f"Retrieved and displayed {len(all_documents['ids'])} documents.")
        except Exception as error:
            logger.error(f"Error viewing all documents: {error}")
            raise

    def delete_all_documents(self):
        try:
            # Recupera tutti gli ID dei documenti nella collezione
            all_documents = self.collection.get()
            document_ids = all_documents.get("ids", [])

            if document_ids:
                # Elimina tutti i documenti specificando gli ID
                self.collection.delete(ids=document_ids)

                # Verifica che tutti i documenti siano stati rimossi
                remaining_documents = self.collection.get()
                if remaining_documents and remaining_documents.get("ids"):
                    logger.error("Some documents or IDs were not removed correctly.")
                else:
                    logger.info("All documents and IDs successfully removed from the vector store.")
            else:
                logger.info("No documents found to remove.")

        except Exception as error:
            logger.error(f"Error removing all documents from vector store: {error}")
            raise





    def similarity_search(self, query, k=2):
        # Esegui una ricerca di similarità
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
        )

        # logger.info(f"Similarity search results: {results}")     # DEBUG

        # Perchè funzioni correttamente, il database vettoriale deve contenere documenti che hanno il campo "metadata" diverso da None

        # Converte i risultati in oggetti Document
        langchain_docs = []
        for i in range(len(results['documents'])):
            for j in range(len(results['documents'][i])):
                document = results['documents'][i][j]
                metadata = results['metadatas'][i][j]
                langchain_docs.append(Document(page_content=document, metadata=metadata))

        logger.info(f"Converted documents: {langchain_docs}")

        return langchain_docs