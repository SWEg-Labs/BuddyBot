from abc import ABC, abstractmethod
from models.question import Question
from models.answer import Answer
from models.header import Header
from models.document import Document

class GenerateAnswerPort(ABC):

    @abstractmethod
    def generate_answer(self, user_input: Question, relevant_docs: list[Document], header: Header) -> Answer:
        pass