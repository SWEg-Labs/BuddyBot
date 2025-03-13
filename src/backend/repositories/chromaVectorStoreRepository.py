import chromadb
import pytz

from models.loggingModels import VectorStoreLog
from entities.chromaDocumentEntity import ChromaDocumentEntity
from entities.queryResultEntity import QueryResultEntity
from utils.logger import logger
from datetime import datetime
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
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

    def __init__(self, collection: chromadb.Collection):
        """ 
        Initializes the ChromaVectorStoreRepository by connecting to the Chroma server and setting up the collection.
        Args:
            collection (chromadb.Collection): The collection object to interact with Chroma.
        """
        self.__collection = collection

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
            '''
            incoming_ids = [doc.get_metadata()["doc_id"] for doc in documents]
            incoming_documents_content = [doc.get_page_content() for doc in documents]
            incoming_metadatas = [doc.get_metadata() for doc in documents]
            incoming_update_time = [doc.get_metadata()["vector_store_insertion_date"] for doc in documents] #sbagliato, serve la data in cui è stato modificato, non quella in cui è stato "vettorizzato"
            '''
            incoming_docs = {doc.get_metadata()["doc_id"]: (doc.get_metadata(),doc.get_page_content()) for doc in documents}

            # Initialize counters
            num_modified_items = 0
            num_deleted_items = 0
            num_added_items = 0

            # Fetch all ids and vector_store_insertion_date from db
            db_docs = {id: date for id, date in self.__collection.get(include=["ids", "last_update"])}

            # Create list of ids to be deleted from db
            try:
                db_ids_to_delete = [id for id in db_docs.keys() if id not in incoming_docs.keys()]
                num_deleted_items += len(db_ids_to_delete)

                for id in db_ids_to_delete:
                    db_docs.pop(id)

            except Exception as e:
                logger.error(f"Error checking for obsolete documents: {e}")

            # Create list of docs to be added to db from incoming
            try:
                incoming_docs_to_add = {id:value for id,value in incoming_docs.items() if id not in db_docs.keys()}
                num_added_items += len(incoming_docs_to_add)
                
                for id in incoming_docs_to_add.keys():
                    incoming_docs.pop(id)

            except Exception as e:
                logger.error(f"Error checking for new documents: {e}")

            # Tolti tutti gli elementi presenti in db e non in incoming, tolti tutti gli elementi presenti in incoming e non in db, rimangono solo gli elementi presenti in entrambi

            # Create list of ids to be updated

            try:
                for incoming_id, incoming_value in incoming_docs.items():
                    if incoming_id in db_docs and incoming_value[0]["last_update"] > db_docs[incoming_id]:
                        db_ids_to_delete.append(incoming_id)
                        db_docs.pop(incoming_id) #operazione inutile, per mantenere coerenza
                        incoming_docs_to_add[incoming_id] = incoming_value
                        num_modified_items += 1
            except Exception as e:
                logger.error(f"Error checking for modified documents: {e}")

            # Delete documents from db
            try:
                self.__collection.delete(ids=db_ids_to_delete)
            except Exception as e:
                logger.error(f"Error deleting documents from db: {e}")

            # Add documents to db
            try:
                self.__collection.add(
                    ids=[id for id in incoming_docs_to_add.keys()],
                    documents=[doc[1] for doc in incoming_docs_to_add.values()],
                    metadatas=[doc[0] for doc in incoming_docs_to_add.values()],
                    vector_store_insertion_dates=[doc[0]["last_update"] for doc in incoming_docs_to_add.values()]
                )
            except Exception as e:
                logger.error(f"Error adding documents to db: {e}")     
           
            '''
            # Check and delete existing documents with the same IDs
            for doc_id in ids:
                try:
                    # Check if document exists by trying to retrieve it
                    existing_docs = self.__collection.get(ids=[doc_id])
                    if existing_docs and len(existing_docs.get('ids', [])) > 0:
                        # Document exists, delete it
                        self.__collection.delete(ids=[doc_id])
                        num_modified_items += 1
                        logger.info(f"Deleted existing document with ID: {doc_id} for update")
                except Exception as e:
                    logger.error(f"Error checking document existence: {e}")
                    raise e

            # Check for documents in collection that are not in the current batch
            try:
                all_docs = self.__collection.get()
                all_ids = all_docs.get('ids', []) if all_docs else []

                for existing_id in all_ids:
                    if existing_id not in ids:
                        # This document is not in the new batch, delete it
                        self.__collection.delete(ids=[existing_id])
                        num_deleted_items += 1
                        logger.info(f"Deleted obsolete document with ID: {existing_id}")
            except Exception as e:
                logger.error(f"Error checking for obsolete documents: {e}")
                raise e

            self.__collection.add(
                ids=ids,
                documents=documents_content,
                metadatas=metadatas
            )
            '''
            
            logger.info(f"Successfully loaded {len(documents)} documents into Chroma vector store.")
            italy_tz = pytz.timezone('Europe/Rome')
            log = VectorStoreLog(
                timestamp=datetime.now(italy_tz),
                outcome=True,
                num_added_items=num_added_items, #len(documents) - num_modified_items,
                num_modified_items=num_modified_items,
                num_deleted_items=num_deleted_items
            )

            return log
        except Exception as e:
            logger.error(f"Error loading documents into Chroma vector store: {e}")
            italy_tz = pytz.timezone('Europe/Rome')
            log = VectorStoreLog(
                timestamp=datetime.now(italy_tz),
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
            query_result = self.__collection.query(
                query_texts=[query],
                n_results=500,
            )

            query_result_entity = QueryResultEntity(
                documents=query_result.get("documents", []),
                metadatas=query_result.get("metadatas", []),
                distances=query_result.get("distances", [])
            )

            logger.info(f"Successfully performed similarity search for query: {query}")

            return query_result_entity
        except Exception as e:
            logger.error(f"Error performing similarity search in ChromaVectorStoreRepository: {e}")
            raise e
