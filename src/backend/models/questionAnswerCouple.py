from models.question import Question
from models.answer import Answer
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
class QuestionAnswerCouple:
    def __init__(self, question: Question, answer: Answer):
        self.__question = question
        self.__answer = answer

    def get_question(self) -> Question:
        return self.__question

    def get_answer(self) -> Answer:
        return self.__answer

    def __eq__(self, other):
        if not isinstance(other, QuestionAnswerCouple):
            return False
        return self.__question == other.get_question() and self.__answer == other.get_answer()
