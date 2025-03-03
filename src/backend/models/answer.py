class Answer:
    def __init__(self, content: str):
        self.__content = content

    def get_content(self) -> str:
        return self.__content

    def __eq__(self, other) -> bool:
        if isinstance(other, Answer):
            return self.__content == other.get_content()
        return False