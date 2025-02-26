from models.question import Question
from models.answer import Answer
from models.header import Header
from models.document import Document
from entities.langChainDocumentEntity import LangChainDocumentEntity
from repositories.langChainRepository import LangChainRepository

class LangChainAdapter:
    def __init__(self, langchain_repository: LangChainRepository):
            self.langchain_repository = langchain_repository

    def generate_answer(self, user_input: Question, relevant_docs: list[Document], header: Header) -> Answer:

        # Adapt the parameters to the format expected by LangChainRepository
        user_input = user_input.content
        relevant_docs = [
            LangChainDocumentEntity(page_content=doc.page_content, metadata=doc.metadata)
            for doc in relevant_docs
        ]
        header = header.content

        # Call the generate_answer method of LangChainRepository
        generated_answer = self.langchain_repository.generate_answer(user_input, relevant_docs, header)

        # Create an Answer object with the generated answer content
        answer = Answer(content=generated_answer)

        return answer

    #def get_next_possible_questions(self, question_answer_couple: QuestionAnswerCouple, header: Header) -> PossibleQuestions:
        # Implement the logic to get the next possible questions based on question_answer_couple and header
    #    pass