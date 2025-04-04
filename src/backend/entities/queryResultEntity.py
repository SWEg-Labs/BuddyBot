from utils.beartype_personalized import beartype_personalized

@beartype_personalized
class QueryResultEntity:
    def __init__(self, documents: list = None, metadatas: list = None, distances: list = None):
        self.__documents = documents if documents is not None else []
        self.__metadatas = metadatas if metadatas is not None else []
        self.__distances = distances if distances is not None else []

    def get_documents(self) -> list:
        return self.__documents

    def get_metadatas(self) -> list:
        return self.__metadatas

    def get_distances(self) -> list:
        return self.__distances

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self) -> dict:
        return {
            "documents": self.__documents,
            "metadatas": self.__metadatas,
            "distances": self.__distances
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            documents=data.get("documents", []),
            metadatas=data.get("metadatas", []),
            distances=data.get("distances", [])
        )
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, QueryResultEntity):
            return False
        return (self.__documents == other.documents and
                self.__metadatas == other.metadatas and
                self.__distances == other.distances)
