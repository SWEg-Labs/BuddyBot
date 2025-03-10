from abc import ABC, abstractmethod

from models.question import Question
from models.answer import Answer
from models.header import Header
from models.document import Document

class GenerateAnswerPort(ABC):
    """
    An abstract base class that defines the interface for generating answers based on user input,
    relevant documents, and a header.
    Methods
        generate_answer(user_input: Question, relevant_docs: list[Document], header: Header) -> Answer
            Abstract method to generate an answer.
    """

    @abstractmethod
    def generate_answer(self, user_input: Question, relevant_docs: list[Document], header: Header) -> Answer:
        """
        Generate an answer based on the provided user input, relevant documents, and header.
        Parameters
            user_input : Question
                The question or input provided by the user.
            relevant_docs : list[Document]
                A list of documents that are relevant to the user's question.
            header : Header
                Additional header information that may be required for generating the answer.
        Returns
            Answer
                The generated answer based on the provided inputs.
        """
        pass