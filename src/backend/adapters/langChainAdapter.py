from business_data_classes import Question, Answer, Header, Document
from backend.repositories.langChainRepository import LangChainRepository

class LangChainAdapter:
    def __init__(self, langchain_repository: LangChainRepository):
            self.langchain_repository = langchain_repository

    def generate_answer(self, user_input: Question, relevant_docs: list[Document], header: Header) -> Answer:

        # Call the generate_answer method of LangChainRepository
        generated_answer = self.langchain_repository.generate_answer(user_input, relevant_docs, header)

        # Create an Answer object with the generated answer content
        answer = Answer(content=generated_answer)

        return answer

    #def get_next_possible_questions(self, question_answer_couple: QuestionAnswerCouple, header: Header) -> PossibleQuestions:
        # Implement the logic to get the next possible questions based on question_answer_couple and header
    #    pass