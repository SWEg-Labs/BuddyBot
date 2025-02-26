class Answer:
    def __init__(self, content: str):
        self.content = content

    def __eq__(self, other):
        if isinstance(other, Answer):
            return self.content == other.content
        return False