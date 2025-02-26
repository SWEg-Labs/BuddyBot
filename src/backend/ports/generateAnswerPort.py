from abc import ABC, abstractmethod
from business_data_classes import Question, Answer, Header, Document

class GenerateAnswerPort(ABC):

    @abstractmethod
    def generate_answer(self, user_input: Question, relevant_docs: list[Document], header: Header) -> Answer:
        pass