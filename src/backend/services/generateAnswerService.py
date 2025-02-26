from models.question import Question
from models.answer import Answer
from models.header import Header
from models.document import Document
from ports.generateAnswerPort import GenerateAnswerPort

class GenerateAnswerService:
    def __init__(self, header: Header, generate_answer_port: GenerateAnswerPort):
        self.header = header
        self.generate_answer_port = generate_answer_port

    def generate_answer(self, user_input: Question, relevant_docs: list[Document]) -> Answer:
        answer = self.generate_answer_port.generate_answer(user_input, relevant_docs, self.header)
        return answer
