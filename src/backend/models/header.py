class Header:
    def __init__(self, content: str):
        self.content = content

    def __eq__(self, other) -> bool:
        if isinstance(other, Header):
            return self.content == other.content
        return False