from utils.beartype_personalized import beartype_personalized

@beartype_personalized
class Header:
    def __init__(self, content: str):
        self.__content = content

    def get_content(self) -> str:
        return self.__content

    def __eq__(self, other) -> bool:
        if isinstance(other, Header):
            return self.__content == other.get_content()
        return False
