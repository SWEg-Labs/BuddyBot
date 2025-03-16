from utils.beartype_personalized import beartype_personalized

@beartype_personalized
class Page:
    def __init__(self, value: int):
        self.__value = value

    def get_value(self) -> int:
        return self.__value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Page):
            return False
        return self.__value == other.get_value()
