from unittest.mock import MagicMock
from langchain_core.documents import Document
from services.generateAnswerService import GenerateAnswerService
from ports.generateAnswerPort import GenerateAnswerPort
from models.header import Header
from models.question import Question
from models.answer import Answer

# Verifica che il metodo generate_answer di GenerateAnswerService chiami il metodo generate_answer di GenerateAnswerPort

def test_generate_answer_calls_port_method():
    # Arrange
    mock_generate_answer_port = MagicMock(spec=GenerateAnswerPort)
    header = Header(attribute="test_header")
    generate_answer_service = GenerateAnswerService(mock_generate_answer_port, header)
    user_input = Question(content="test question")
    relevant_docs = [
        Document(page_content="doc1"),
        Document(page_content="doc2"),
    ]
    expected_answer = Answer(content="test answer")
    mock_generate_answer_port.generate_answer.return_value = expected_answer

    # Act
    result = generate_answer_service.generate_answer(user_input, relevant_docs)

    # Assert
    mock_generate_answer_port.generate_answer.assert_called_once_with(user_input, relevant_docs, header)
    assert result == expected_answer