import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from langchain_core.documents import Document
from utils.logger import logger

class VectorStoreRepository:
    def __init__(self):
        try:
            # Connessione al server ChromaDB
            self.client = chromadb.HttpClient(host=os.getenv("CHROMA_HOST", "localhost"),
                                              port=int(os.getenv("CHROMA_PORT", "8000")))
            self.client.heartbeat()  # Verifica connessione

            self.collection_name = "buddybot-vector-store"
            self.max_chunk_size = 41666  # 42KB

            # Crea o ottieni una collezione esistente
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name
            )
            logger.info("Successfully connected to Chroma vector store.")
        except Exception as e:
            logger.error(f"Error initializing Chroma vector store: {e}")
            raise

    def _split_github_documents(self, documents):
        """
        Splits GitHub documents into chunks of a maximum size of self.max_chunk_size characters.
        """
        try:
            split_docs = []
            for doc in documents:
                content = doc.page_content
                metadata = doc.metadata
                for i in range(0, len(content), self.max_chunk_size):
                    chunk_content = content[i:i+self.max_chunk_size]
                    chunk_metadata = metadata.copy()
                    chunk_metadata["chunk_index"] = i // self.max_chunk_size
                    split_docs.append(Document(page_content=chunk_content, metadata=chunk_metadata))
            logger.info(f"GitHub documents split into {len(split_docs)} chunks.")
            return split_docs
        except Exception as e:
            logger.error(f"Error splitting GitHub documents: {e}")
            raise

    def add_github_documents(self, documents):
        """
        Adds GitHub documents to the Chroma database after splitting them into chunks.
        """
        try:
            split_docs = self._split_github_documents(documents)
            for doc in split_docs:
                self.collection.add(
                    documents=[doc.page_content],
                    metadatas=[doc.metadata],
                    ids=[doc.metadata["id"]],
                )
            logger.info("GitHub documents added successfully to vector store.")
        except Exception as e:
            logger.error(f"Error adding GitHub documents to vector store: {e}")
            raise

    def _split_jira_issues(self, issues):
        """
        Splits Jira issues into chunks of a maximum size of self.max_chunk_size characters.
        """
        try:
            split_issues = []
            for issue in issues:
                assignee = issue["fields"].get("assignee")
                if assignee:
                    assignee_name = assignee["displayName"]
                else:
                    assignee_name = ""  # Default to empty string if assignee is not present (NoneType)

                content = issue["fields"]["summary"]
                metadata = {
                    "project": issue["fields"]["project"]["name"],
                    "status": issue["fields"]["status"]["name"],
                    "assignee": assignee_name,
                    "priority": issue["fields"]["priority"]["name"],
                    "id": issue["key"],
                }

                for i in range(0, len(content), self.max_chunk_size):
                    chunk_content = content[i:i+self.max_chunk_size]
                    chunk_metadata = metadata.copy()
                    chunk_metadata["chunk_index"] = i // self.max_chunk_size
                    split_issues.append({"page_content": chunk_content, "metadatas": chunk_metadata})

            logger.info(f"Jira issues split into {len(split_issues)} chunks.")
            return split_issues
        except Exception as e:
            logger.error(f"Error splitting Jira issues: {e}")
            raise

    def add_jira_issues(self, issues):
        """
        Adds Jira issues to the Chroma database after splitting them into chunks.
        """
        try:
            split_issues = self._split_jira_issues(issues)
            for issue in split_issues:
                self.collection.add(
                    documents=[issue["page_content"]],
                    metadatas=[issue["metadatas"]],
                    ids=[issue["metadatas"]["id"]],
                )
            logger.info("Jira issues added successfully to Chroma database.")
        except Exception as e:
            logger.error(f"Error adding Jira issues to Chroma database: {e}")
            raise

    def _split_confluence_pages(self, pages):
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.max_chunk_size, chunk_overlap=0)
            split_pages = []
            for page in pages:
                split_content = text_splitter.split_text(page["body"]["storage"]["value"])
                for chunk in split_content:
                    metadata = {
                        "title": page["title"],
                        "page_id": page["id"]
                    }
                    if page.get("version"):
                        metadata.update({
                            "created_by": page["version"].get("createdBy", {}).get("displayName", ""),
                            "created_date": page["version"].get("created", "")
                        })
                    split_pages.append({
                        "page_content": chunk,
                        "metadata": metadata
                    })
            logger.info(f"Confluence pages split into {len(split_pages)} chunks.")
            return split_pages
        except Exception as e:
            logger.error(f"Error splitting Confluence pages: {e}")
            raise

    def add_confluence_pages(self, pages):
        try:
            split_pages = self._split_confluence_pages(pages)
            for page in split_pages:
                self.collection.add(
                    documents=[page["page_content"]],
                    metadatas=[page["metadata"]],
                    ids=[page["metadata"]["page_id"]],
                )
            logger.info("Confluence pages added successfully to vector store.")
        except Exception as e:
            logger.error(f"Error adding Confluence pages to vector store: {e}")
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
        except Exception as e:
            logger.error(f"Error viewing all documents: {e}")
            raise

    def delete_and_recreate_collection(self):
        """
        Deletes the entire collection with the name self.collection_name and recreates it as an empty collection.
        """
        try:
            # Delete the collection
            self.client.delete_collection(name=self.collection_name)
            logger.info(f"Collection '{self.collection_name}' successfully deleted.")

            # Recreate the collection
            self.collection = self.client.create_collection(name=self.collection_name)
            logger.info(f"Collection '{self.collection_name}' successfully recreated.")
        except Exception as e:
            logger.error(f"Error deleting and recreating the collection: {e}")
            raise

    def similarity_search(self, query, k=2):
        try:
            # Esegui una ricerca di similarità
            results = self.collection.query(
                query_texts=[query],
                n_results=k,
            )

            # logger.info(f"Similarity search results: {results}")     # DEBUG

            # Converte i risultati in oggetti Document
            # Perchè funzioni correttamente, il database vettoriale deve contenere documenti che hanno il campo "metadata" diverso da None
            langchain_docs = []
            for i in range(len(results['documents'])):
                for j in range(len(results['documents'][i])):
                    document = results['documents'][i][j]
                    metadata = results['metadatas'][i][j]
                    langchain_docs.append(Document(page_content=document, metadata=metadata))

            # logger.info(f"Converted documents: {langchain_docs}")     # DEBUG

            return langchain_docs
        except Exception as e:
            logger.error(f"Error performing similarity search: {e}")
            raise