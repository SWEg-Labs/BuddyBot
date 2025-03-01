from models.question import Question
from models.document import Document
from models.loggingModels import VectorStoreLog
from entities.chromaDocumentEntity import ChromaDocumentEntity
from ports.similaritySearchPort import SimilaritySearchPort
from ports.loadFilesInVectorStorePort import LoadFilesInVectorStorePort
from repositories.chromaVectorStoreRepository import ChromaVectorStoreRepository
from utils.logger import logger
from datetime import datetime

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
        self.max_chunk_size = max_chunk_size
        self.chroma_vector_store_repository = chroma_vector_store_repository

    def load(self, documents: list[Document]) -> VectorStoreLog:
        """
        Loads the given documents into the Chroma vector store after splitting them into chunks.
        Args:
            documents (list[Document]): List of documents to be loaded.
        Returns:
            VectorStoreLog: Log of the load operation, including the outcome and number of items added, modified, and deleted.
        """
        try:
            chroma_documents = self.split(documents)
            result = self.chroma_vector_store_repository.load(chroma_documents)
            return result
        except Exception as e:
            logger.error(f"Error in adapting Documents to load: {e}")
            return VectorStoreLog(
                timestamp=datetime.now(),
                outcome=False,
                num_added_items=0,
                num_modified_items=0,
                num_deleted_items=0
            )

    def split(self, documents: list[Document]) -> list[ChromaDocumentEntity]:
        """
        Splits the given documents into chunks based on the maximum chunk size.
        Args:
            documents (list[Document]): List of documents to be split.
        Returns:
            list[ChromaDocumentEntity]: List of document chunks as ChromaDocumentEntity objects.
        """
        try:
            chroma_documents = []
            for document in documents:
                page_content = document.get_page_content()
                metadata = document.get_metadata()
                doc_id = metadata.get("id", "")
                chunks = [page_content[i:i + self.max_chunk_size] for i in range(0, len(page_content), self.max_chunk_size)]
                
                for chunk_index, chunk in enumerate(chunks):
                    chunk_metadata = metadata.copy()
                    chunk_metadata["chunk_index"] = chunk_index
                    chunk_metadata["doc_id"] = f"{doc_id}_{chunk_index}"
                    chunk_metadata["vector_store_insertion_date"] = datetime.now().isoformat()
                    chroma_documents.append(ChromaDocumentEntity(page_content=chunk, metadata=chunk_metadata))

            return chroma_documents
        except Exception as e:
            logger.error(f"Error in splitting Documents: {e}")
            return []

    def similarity_search(self, user_input: Question) -> list[Document]:
        """
        Performs a similarity search on the Chroma vector store using the given user input.
        Args:
            user_input (Question): The user input question for the similarity search.
        Returns:
            list[Document]: List of documents that are similar to the user input.
        """
        try:
            query_result_entity = self.chroma_vector_store_repository.similarity_search(user_input.content)

            relevant_docs = []
            # Per scalabilità creo un for anche per le queries, nonostante sia sempre una sola, avente indice i=0
            for i in range(len(query_result_entity['documents'])):           # Indice i: va da 0 a (numero di query - 1)
                for j in range(len(query_result_entity['documents'][i])):    # Indice j: va da 0 a (numero di risultati trovati in risposta alla query i-esima - 1)
                    document = query_result_entity['documents'][i][j]
                    metadata = query_result_entity['metadatas'][i][j]
                    distance = query_result_entity['distances'][i][j]
                    
                    # Aggiungi la distanza come metadato
                    metadata["distance"] = distance

                    # Aggiungi il documento alla lista dei risultati
                    relevant_docs.append(Document(page_content=document, metadata=metadata))

            return relevant_docs
        except Exception as e:
            logger.error(f"Error in ChromaVectorStoreAdapter: {e}")
            raise e
