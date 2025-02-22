from abc import ABC, abstractmethod

class ChatUseCase(ABC):
    """
    Interface for chat use cases.
    """

    @abstractmethod
    def process_user_input(self, user_input: str) -> str:
        """
        Processes the user's input and generates a response.

        Args:
            user_input (str): The input provided by the user.

        Returns:
            str: The generated response.
        """
        pass

