class Quantity:
    def __init__(self, value: int) -> None:
        self.value = value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Quantity):
            return False
        return self.value == other.value
    
