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
        This method also handles:
         - Identifying obsolete documents (present in Chroma but not among the incoming ones).
         - Preparing new documents (not already present in Chroma).
         - For updates of non-GitHub File documents, if the "last_update" field of the incoming document is more recent,
           the document is considered updated (modified).
         - For GitHub Files, the "creation_date" field (incoming) is compared with the "insertion_date" field (DB) to determine
           whether the file should be counted as "added" or "modified".
        Args:
            documents (list[ChromaDocumentEntity]): A list of documents to be loaded.
        Returns:
            VectorStoreLog: An object containing the log of the operation.
        
        Raises:
            Exception: If an error occurs while loading the documents.
        """
        try:
            date_format = "%Y-%m-%dT%H:%M:%S"

            # Preparazione dei documenti in arrivo: mappatura doc_id -> (metadata, page_content)
            try:
                incoming_docs = {
                    doc.get_metadata()["doc_id"]: (doc.get_metadata(), doc.get_page_content())
                    for doc in documents
                }
            except Exception as e:
                logger.error(f"Error preparing new data for update: {e}")
                raise e

            # Inizializza i contatori
            num_added_items = 0
            num_modified_items = 0
            num_deleted_items = 0

            # Fetch dei documenti già presenti in Chroma
            try:
                db_docs = {}
                chroma_data = self.__collection.get(include=["metadatas"])
                i = 0
                for doc_id in chroma_data['ids']:
                    db_docs[doc_id] = chroma_data['metadatas'][i]
                    i += 1
            except Exception as e:
                logger.error(f"Error getting old data from chroma: {e}")
                raise e

            logger.info(f"Fetched {len(db_docs)} documents from Chroma vector store.")

            # Creazione della lista degli id da eliminare: documenti presenti in DB ma non negli incoming
            try:
                db_ids_to_delete = [doc_id for doc_id in db_docs.keys() if doc_id not in incoming_docs.keys()]
                num_deleted_items += len(db_ids_to_delete)
                for doc_id in db_ids_to_delete:
                    db_docs.pop(doc_id)
            except Exception as e:
                logger.error(f"Error checking for obsolete documents: {e}")

            # Creazione del dizionario dei documenti da aggiungere: quelli presenti negli incoming ma non in DB
            try:
                incoming_docs_to_add = {
                    doc_id: value for doc_id, value in incoming_docs.items() if doc_id not in db_docs.keys()
                }
                num_added_items += len(incoming_docs_to_add)
                for doc_id in list(incoming_docs_to_add.keys()):
                    incoming_docs.pop(doc_id)
            except Exception as e:
                logger.error(f"Error checking for new documents: {e}")

            # Tolti tutti gli elementi presenti in db e non in incoming, tolti tutti gli elementi presenti in incoming e non in db,
            # rimangono solo gli elementi presenti in entrambi.

            # -------------------------------------------------------------------------------
            # Sezione: Aggiornamento per documenti NON GitHub File
            # -------------------------------------------------------------------------------
            try:
                for incoming_id, incoming_value in list(incoming_docs.items()):
                    metadata = incoming_value[0]
                    # Se non è un GitHub File, procedi con il confronto delle date "last_update"
                    if metadata.get("item_type") == "GitHub File":
                        continue
                    try:
                        incoming_last_update = datetime.strptime(
                            metadata.get("last_update"), date_format
                        )
                        db_last_update = datetime.strptime(
                            db_docs[incoming_id]["last_update"], date_format
                        )
                    except Exception as e:
                        logger.error(f"Error parsing datetime for doc_id {incoming_id}: {e}")
                        raise e

                    if incoming_last_update > db_last_update:
                        # Il documento è stato aggiornato: verrà inserito in Chroma, e conta come modified.
                        db_ids_to_delete.append(incoming_id)
                        num_modified_items += 1
                        incoming_docs_to_add[incoming_id] = incoming_value
                        incoming_docs.pop(incoming_id)
            except Exception as e:
                logger.error(f"Error checking for modified documents: {e}")
                raise e
            # Fine sezione aggiornamenti non GitHub File.

            # -------------------------------------------------------------------------------
            # Sezione: Controllo specifico per i GitHub File
            # Confronta "creation_date" (incoming) con "insertion_date" (DB) per stabilire se il file è aggiunto o modificato.
            # -------------------------------------------------------------------------------
            try:
                # Costruiamo una mapping per i GitHub File già presenti in Chroma basata sul campo "path"
                db_github_by_path = {}
                for db_id, metadata in db_docs.items():
                    if metadata.get("item_type") == "GitHub File":
                        path = metadata.get("path")
                        if path:
                            db_github_by_path[path] = metadata

                for incoming_id, incoming_value in incoming_docs.items():
                    metadata = incoming_value[0]
                    if metadata.get("item_type") != "GitHub File":
                        continue
                    path = metadata.get("path")
                    if not path:
                        continue
                    if path in db_github_by_path:
                        db_metadata = db_github_by_path[path]
                        try:
                            incoming_creation_date = datetime.strptime(
                                metadata.get("creation_date"), date_format
                            )
                            db_insertion_date = datetime.strptime(
                                db_metadata.get("insertion_date"), date_format
                            )
                        except Exception as e:
                            logger.error(f"Error parsing dates for GitHub File with path {path}: {e}")
                            continue
                        if incoming_creation_date > db_insertion_date:
                            num_added_items += 1
                        else:
                            num_modified_items += 1
            except Exception as e:
                logger.error(f"Error checking for GitHub File modifications: {e}")
                raise e

            # -------------------------------------------------------------------------------
            # Aggiornamento del DB: eliminazione e aggiunta dei documenti identificati
            # -------------------------------------------------------------------------------
            try:
                if db_ids_to_delete:
                    self.__collection.delete(ids=db_ids_to_delete)
            except Exception as e:
                logger.error(f"Error deleting documents from db: {e}")

            logger.info(f"Deleted {num_deleted_items} documents from Chroma vector store.")

            try:
                if incoming_docs_to_add:
                    self.__collection.add(
                        ids=[doc_id for doc_id in incoming_docs_to_add.keys()],
                        documents=[doc[1] for doc in incoming_docs_to_add.values()],
                        metadatas=[doc[0] for doc in incoming_docs_to_add.values()],
                    )
            except Exception as e:
                logger.error(f"Error adding documents to db: {e}")

            logger.info(f"Successfully loaded documents into Chroma vector store. "
                        f"Added: {num_added_items}, Modified: {num_modified_items}.")

            italy_tz = pytz.timezone('Europe/Rome')
            log = VectorStoreLog(
                timestamp=datetime.now(italy_tz),
                outcome=True,
                num_added_items=num_added_items,
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
