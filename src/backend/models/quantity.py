class Quantity:
    def __init__(self, value: int):
        self.__value = value

    def get_value(self) -> int:
        return self.__value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Quantity):
            return False
        return self.__value == other.get_value()
