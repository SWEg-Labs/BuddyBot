import pytest
from unittest.mock import MagicMock

from models.document import Document
from models.header import Header
from models.question import Question
from services.generateAnswerService import GenerateAnswerService
from ports.generateAnswerPort import GenerateAnswerPort


# Verifica che il metodo generate_answer di GenerateAnswerService gestisca correttamente le eccezioni

def test_generate_answer_handles_exception():
    # Arrange
    header = Header(content="test_header")
    mock_generate_answer_port = MagicMock(spec=GenerateAnswerPort)
    generate_answer_service = GenerateAnswerService(header, mock_generate_answer_port)
    user_input = Question(content="test question")
    relevant_docs = [
        Document(page_content="doc1"),
        Document(page_content="doc2"),
    ]
    mock_generate_answer_port.generate_answer.side_effect = Exception("Generate answer error")

    # Act
    with pytest.raises(Exception) as exc_info:
        generate_answer_service.generate_answer(user_input, relevant_docs)

    # Assert
    assert str(exc_info.value) == "Generate answer error"
    mock_generate_answer_port.generate_answer.assert_called_once_with(user_input, relevant_docs, header)
