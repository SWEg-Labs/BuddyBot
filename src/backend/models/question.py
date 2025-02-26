class Question:
    def __init__(self, content: str):
        self.content = content

    def __eq__(self, other):
        if isinstance(other, Question):
            return self.content == other.content
        return False