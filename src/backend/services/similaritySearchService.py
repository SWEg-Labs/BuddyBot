from langchain_core.documents import Document
from ports.similaritySearchPort import SimilaritySearchPort

class SimilaritySearchService:
    def __init__(self, similarity_search_port: SimilaritySearchPort):
        self.similarity_search_port = similarity_search_port

    def similarity_search(self, user_input: str) -> list[Document]:
        similarity_threshold = 1.2
        max_gap = 0.3
        relevant_docs = []
        previous_distance = None

        documents = self.similarity_search_port.similarity_search(user_input)
        for document in documents:
            distance = document.metadata.get("distance", 1.0)

            # Controlla la soglia di similarità
            if distance > similarity_threshold:
                continue  # Salta il documento se supera la soglia

            # Controlla il distacco massimo
            if previous_distance is not None and abs(distance - previous_distance) > max_gap:
                return relevant_docs  # Termina e restituisce i documenti trovati finora

            # Aggiungi il documento alla lista dei risultati
            relevant_docs.append(Document(page_content=document.page_content, metadata=document.metadata))

            # Aggiorna la distanza precedente
            previous_distance = distance

        return relevant_docs