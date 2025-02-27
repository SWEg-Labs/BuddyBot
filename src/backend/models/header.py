class Header:
    def __init__(self, content: str):
        self.content = content

    def __eq__(self, other):
        if isinstance(other, Header):
            return self.content == other.content
        return False