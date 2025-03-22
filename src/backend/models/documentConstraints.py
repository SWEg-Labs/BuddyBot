from utils.beartype_personalized import beartype_personalized

@beartype_personalized
class DocumentConstraints:
    def __init__(self, similarity_threshold: float, max_gap: float):
        self.__similarity_threshold = similarity_threshold
        self.__max_gap = max_gap

    def get_similarity_threshold(self) -> float:
        return self.__similarity_threshold

    def get_max_gap(self) -> float:
        return self.__max_gap
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DocumentConstraints):
            return False
        return self.__similarity_threshold == other.get_similarity_threshold() and self.__max_gap == other.get_max_gap()
