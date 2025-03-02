class DocumentConstraints:
    def __init__(self, similarity_threshold: float, max_gap: float):
        self.__similarity_threshold = similarity_threshold
        self.__max_gap = max_gap