from business_data_classes import Question, Answer, Header, Document
from ports import GenerateAnswerPort

class GenerateAnswerService:
    def __init__(self, header: Header):
        self.header = header

    def generate_answer(self, user_input: Question, relevant_docs: list[Document]) -> Answer:
        generate_answer_port = GenerateAnswerPort()
        answer = generate_answer_port.generate_answer(user_input, relevant_docs, self.header)
        return answer
