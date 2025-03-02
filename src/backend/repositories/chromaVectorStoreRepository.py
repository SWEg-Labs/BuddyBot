import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb

from models.loggingModels import VectorStoreLog
from entities.chromaDocumentEntity import ChromaDocumentEntity
from entities.queryResultEntity import QueryResultEntity
from utils.logger import logger
from datetime import datetime

class ChromaVectorStoreRepository:
    """
    A repository class for interacting with the Chroma vector store.
    This class provides methods to initialize the connection, load documents, and perform similarity searches.

    Attributes:
        client (chromadb.HttpClient): The client to connect to the Chroma server.
        collection_name (str): The name of the collection in the Chroma.
        collection (chromadb.Collection): The collection object to interact with the Chroma.

    Raises:
        Exception: If an error occurs during initialization or while interacting with the vector store.
    """

    def __init__(self, chroma_client: chromadb.HttpClient, collection_name: str, collection: chromadb.Collection):
        """ 
        Initializes the ChromaVectorStoreRepository by connecting to the Chroma server and setting up the collection.

        Args:
            chroma_client (chromadb.HttpClient): The client used to connect to the Chroma server.
            collection_name (str): The name of the collection to be used.
            collection (chromadb.Collection): The collection object to be used.

        Raises: 
            Exception: If an error occurs during initialization. 
        """
        try:
            self.client = chroma_client
            self.collection_name = collection_name
            self.collection = collection
            logger.info("Successfully connected to Chroma vector store.")
        except Exception as e:
            logger.error(f"Error initializing Chroma vector store: {e}")
            raise

    def load(self, documents: list[ChromaDocumentEntity]) -> VectorStoreLog:
        """
        Loads the provided documents into the Chroma vector store.

        Args:
            documents (list[ChromaDocumentEntity]): A list of documents to be loaded.

        Returns:
            VectorStoreLog: An object containing the log of the operation.
        
        Raises:
            Exception: If an error occurs while loading the documents.
        """
        try:
            documents_data = [
                {
                    "id": doc.get_metadata()["doc_id"],
                    "content": doc.get_page_content(),
                    "metadata": doc.get_metadata()
                }
                for doc in documents
            ]

            # Carica i documenti nel Chroma vector store
            self.collection.add(documents_data)

            logger.info(f"Successfully loaded {len(documents)} documents into Chroma vector store.")
            log = VectorStoreLog(
                timestamp=datetime.now(),
                outcome=True,
                num_added_items=len(documents),
                num_modified_items=0,
                num_deleted_items=0
            )

            return log
        except Exception as e:
            logger.error(f"Error loading documents into Chroma vector store: {e}")
            log = VectorStoreLog(
                timestamp=datetime.now(),
                outcome=False,
                num_added_items=0,
                num_modified_items=0,
                num_deleted_items=0
            )
            return log

    def similarity_search(self, query: str) -> QueryResultEntity:
        """ 
        Performs a similarity search in the collection and returns the most relevant documents. 
        
        Args: 
            query (str): The query text to search for. 
            
        Returns: 
            QueryResultEntity: An object containing the most relevant documents, their metadata, and distances. 
            
        Raises: 
            Exception: If an error occurs while performing the similarity search. 
        """
        try:
            # Esegui una ricerca di similarità
            query_result = self.collection.query(
                query_texts=[query],
                n_results=10000,
            )

            query_result_entity = QueryResultEntity(
                documents=query_result.get("documents", []),
                metadatas=query_result.get("metadatas", []),
                distances=query_result.get("distances", [])
            )

            logger.info(f"Successfully performed similarity search for query: {query}")

            return query_result_entity
        except Exception as e:
            logger.error(f"Error performing similarity search: {e}")
            raise
