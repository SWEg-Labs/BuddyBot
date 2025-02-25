class QueryResultEntity:
    def __init__(self, documents=None, metadatas=None, distances=None):
        self.documents = documents if documents is not None else []
        self.metadatas = metadatas if metadatas is not None else []
        self.distances = distances if distances is not None else []

    def to_dict(self):
        return {
            "documents": self.documents,
            "metadatas": self.metadatas,
            "distances": self.distances
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            documents=data.get("documents", []),
            metadatas=data.get("metadatas", []),
            distances=data.get("distances", [])
        )