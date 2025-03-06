from datetime import datetime
import pytz

from models.question import Question
from models.document import Document
from models.loggingModels import VectorStoreLog
from entities.chromaDocumentEntity import ChromaDocumentEntity
from ports.similaritySearchPort import SimilaritySearchPort
from ports.loadFilesInVectorStorePort import LoadFilesInVectorStorePort
from repositories.chromaVectorStoreRepository import ChromaVectorStoreRepository
from utils.logger import logger

class ChromaVectorStoreAdapter(SimilaritySearchPort, LoadFilesInVectorStorePort):
    """
    Adapter class for interacting with a Chroma vector store repository.
    This class provides methods to load documents into the vector store,
    split documents into chunks, and perform similarity searches.
    Attributes:
        max_chunk_size (int): Maximum size of each document chunk.
        chroma_vector_store_repository (ChromaVectorStoreRepository): Repository for interacting with the Chroma vector store.
    """

    def __init__(self, max_chunk_size: int, chroma_vector_store_repository: ChromaVectorStoreRepository):
        """
        Initializes the ChromaVectorStoreAdapter with the specified maximum chunk size and repository.
        Args:
            max_chunk_size (int): Maximum size of each document chunk.
            chroma_vector_store_repository (ChromaVectorStoreRepository): Repository for interacting with the Chroma vector store.
        """
        self.__max_chunk_size = max_chunk_size
        self.__chroma_vector_store_repository = chroma_vector_store_repository

    def load(self, documents: list[Document]) -> VectorStoreLog:
        """
        Loads the given documents into the Chroma vector store after splitting them into chunks.
        Args:
            documents (list[Document]): List of documents to be loaded.
        Returns:
            VectorStoreLog: Log of the load operation, including the outcome and number of items added, modified, and deleted.
        """
        try:
            chroma_documents = self.__split(documents)
            result = self.__chroma_vector_store_repository.load(chroma_documents)
            return result
        except Exception as e:
            logger.error(f"Error in adapting documents to load: {e}")
            raise e

    def __split(self, documents: list[Document]) -> list[ChromaDocumentEntity]:
        """
        Splits the given documents into chunks based on the maximum chunk size.
        Args:
            documents (list[Document]): List of documents to be split.
        Returns:
            list[ChromaDocumentEntity]: List of document chunks as ChromaDocumentEntity objects.
        """
        try:
            chroma_documents = []
            seen_doc_ids = set()
            date_format = "%Y-%m-%dT%H:%M:%S"

            for document in documents:
                page_content = document.get_page_content()
                metadata = document.get_metadata()
                doc_id = metadata.get("id", "")

                # Check for duplicate doc_id values
                if doc_id in seen_doc_ids:
                    logger.info(f"Skipping duplicate document with id: {doc_id}")
                    continue
                seen_doc_ids.add(doc_id)

                logger.info(f"Splitting document {doc_id} into chunks...")
                chunks = [page_content[i:i + self.__max_chunk_size] for i in range(0, len(page_content), self.__max_chunk_size)]

                for chunk_index, chunk in enumerate(chunks):
                    chunk_metadata = metadata.copy()

                    # Convert list of files to string
                    if "files" in chunk_metadata and isinstance(chunk_metadata["files"], list):
                        chunk_metadata["files"] = "\n".join(chunk_metadata["files"])

                    # Format dates as strings
                    if "date" in chunk_metadata and hasattr(chunk_metadata["date"], "strftime"):
                        chunk_metadata["date"] = chunk_metadata["date"].strftime(date_format)
                    if "creation_date" in chunk_metadata and hasattr(chunk_metadata["creation_date"], "strftime"):
                        chunk_metadata["creation_date"] = chunk_metadata["creation_date"].strftime(date_format)

                    # Add vector store insertion date
                    italy_tz = pytz.timezone('Europe/Rome')
                    chunk_metadata["vector_store_insertion_date"] = datetime.now(italy_tz).strftime(date_format)

                    # Add chunk metadata
                    chunk_metadata["chunk_index"] = chunk_index
                    chunk_metadata["doc_id"] = f"{doc_id}_{chunk_index}"

                    chroma_documents.append(ChromaDocumentEntity(page_content=chunk, metadata=chunk_metadata))

            return chroma_documents
        except Exception as e:
            logger.error(f"Error in splitting Documents: {e}")
            raise e

    def similarity_search(self, user_input: Question) -> list[Document]:
        """
        Performs a similarity search on the Chroma vector store using the given user input.
        Args:
            user_input (Question): The user input question for the similarity search.
        Returns:
            list[Document]: List of documents that are similar to the user input.
        """
        try:
            query_result_entity = self.__chroma_vector_store_repository.similarity_search(user_input.get_content())

            relevant_docs = []
            # Per scalabilità creo un for anche per le queries, nonostante sia sempre una sola, avente indice i=0
            for i in range(len(query_result_entity.get_documents())):           # Indice i: va da 0 a (numero di query - 1)
                for j in range(len(query_result_entity.get_documents()[i])):    # Indice j: va da 0 a (numero di risultati trovati in risposta alla query i-esima - 1)
                    document = query_result_entity.get_documents()[i][j]
                    metadata = query_result_entity.get_metadatas()[i][j]
                    distance = query_result_entity.get_distances()[i][j]
                    
                    # Aggiungi la distanza come metadato
                    metadata["distance"] = distance

                    # Aggiungi il documento alla lista dei risultati
                    relevant_docs.append(Document(page_content=document, metadata=metadata))

            return relevant_docs
        except Exception as e:
            logger.error(f"Error in adapting documents for similarity_search: {e}")
            raise e
