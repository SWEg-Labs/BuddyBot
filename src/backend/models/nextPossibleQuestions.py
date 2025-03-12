from models.possibleQuestion import PossibleQuestion
from utils.beartype_personalized import beartype_personalized

@beartype_personalized
class NextPossibleQuestions:
    def __init__(self, num_questions: int, possible_questions: list[PossibleQuestion]):
        if len(possible_questions) != num_questions:
            raise ValueError("Il numero di elementi in possible_questions non coincide con num_questions")
        self.__num_questions = num_questions
        self.__possible_questions = possible_questions

    def get_num_questions(self) -> int:
        return self.__num_questions

    def get_possible_questions(self) -> list[PossibleQuestion]:
        return self.__possible_questions

    def __eq__(self, other):
        if not isinstance(other, NextPossibleQuestions):
            return False
        return (self.__num_questions == other.get_num_questions() and
                self.__possible_questions == other.get_possible_questions())
