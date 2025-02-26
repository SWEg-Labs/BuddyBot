from models.question import Question
from models.document import Document
from ports.similaritySearchPort import SimilaritySearchPort
from repositories.chromaVectorStoreRepository import ChromaVectorStoreRepository
from utils.logger import logger

class ChromaVectorStoreAdapter(SimilaritySearchPort):
    def __init__(self, chroma_vector_store_repository: ChromaVectorStoreRepository):
        self.chroma_vector_store_repository = chroma_vector_store_repository

    def similarity_search(self, user_input: Question) -> list[Document]:
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
