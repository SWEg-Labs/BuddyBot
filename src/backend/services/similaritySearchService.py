from models.question import Question
from models.document import Document
from models.documentConstraints import DocumentConstraints
from ports.similaritySearchPort import SimilaritySearchPort
from utils.logger import logger
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
class SimilaritySearchService:
    """
    A service class for performing similarity searches on documents.
    Attributes:
        document_constraints (DocumentConstraints): Constraints to apply during the similarity search.
        similarity_search_port (SimilaritySearchPort): The port used to perform the similarity search.
    """

    def __init__(self, document_constraints: DocumentConstraints, similarity_search_port: SimilaritySearchPort):
        """
        Initializes the SimilaritySearchService with the given document constraints and similarity search port.
        Args:
            document_constraints (DocumentConstraints): Constraints to apply during the similarity search.
            similarity_search_port (SimilaritySearchPort): The port used to perform the similarity search.
        """
        self.__document_constraints = document_constraints
        self.__similarity_search_port = similarity_search_port

    def similarity_search(self, user_input: Question) -> list[Document]:
        """
        Performs a similarity search based on the user input and returns a list of relevant documents.
        Args:
            user_input (Question): The input question for which similar documents are to be searched.
        Returns:
            list[Document]: A list of documents that are relevant to the user input.
        Raises:
            Exception: If an error occurs during the similarity search.
        """
        try:
            similarity_threshold = self.__document_constraints.get_similarity_threshold()
            max_gap = self.__document_constraints.get_max_gap()

            relevant_docs = []
            previous_distance = None

            documents = self.__similarity_search_port.similarity_search(user_input)
            for document in documents:
                distance = document.get_metadata().get("distance")

                # Controlla la soglia di similarità
                if distance > similarity_threshold:
                    continue  # Salta il documento se supera la soglia

                # Controlla il distacco massimo
                if previous_distance is not None and abs(distance - previous_distance) > max_gap:
                    return relevant_docs  # Termina e restituisce i documenti trovati finora

                # Aggiungi il documento alla lista dei risultati
                relevant_docs.append(Document(page_content=document.get_page_content(), metadata=document.get_metadata()))

                # Aggiorna la distanza precedente
                previous_distance = distance

            return relevant_docs
        except Exception as e:
            logger.error(f"Error in similarity search service: {e}")
            raise e
