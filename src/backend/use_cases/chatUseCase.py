from abc import ABC, abstractmethod

from models.question import Question
from models.answer import Answer

class ChatUseCase(ABC):
    """
    Interface for chat use cases.
    """

    @abstractmethod
    def get_answer(self, user_input: Question) -> Answer:
        """
        Processes the user's input and generates an answer.

        Args:
            user_input (Question): The input provided by the user.

        Returns:
            Answer: The generated answer.
        """
        pass

