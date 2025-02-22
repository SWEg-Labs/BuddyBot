from langchain_core.documents import Document
from ports.similarity_search_port import SimilaritySearchPort
from chroma_vector_store_repository import ChromaVectorStoreRepository

class ChromaVectorStoreAdapter(SimilaritySearchPort):
    def __init__(self, chroma_vector_store_repository: ChromaVectorStoreRepository):
        self.chroma_vector_store_repository = chroma_vector_store_repository

    def similarity_search(self, user_input: str) -> list[Document]:
        document_entities = self.chroma_vector_store_repository.similarity_search(user_input)
        documents = [Document(page_content=entity.page_content, metadata=entity.metadata) for entity in document_entities]
        return documents