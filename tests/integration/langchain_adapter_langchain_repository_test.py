from unittest.mock import MagicMock
from models.document import Document
from models.question import Question
from models.header import Header
from models.answer import Answer
from adapters.langChainAdapter import LangChainAdapter
from repositories.langChainRepository import LangChainRepository
from entities.langChainDocumentEntity import LangChainDocumentEntity

# Verifica che il metodo generate_answer di LangChainAdapter chiami il metodo generate_answer di LangChainRepository

def test_generate_answer_calls_repository_method():
    # Arrange
    max_num_tokens = 128000
    mock_langchain_repository = MagicMock(spec=LangChainRepository)
    langchain_adapter = LangChainAdapter(max_num_tokens, mock_langchain_repository)
    user_input = Question("test question")
    relevant_docs = [
        Document(page_content="doc1", metadata={"distance": 0.5}),
        Document(page_content="doc2", metadata={"distance": 0.75}),
    ]
    header = Header("test header")
    langchain_relevant_docs = [
        LangChainDocumentEntity(page_content="Metadata: {'distance': 0.5}\nContent: doc1", metadata={"distance": 0.5}),
        LangChainDocumentEntity(page_content="Metadata: {'distance': 0.75}\nContent: doc2", metadata={"distance": 0.75}),
    ]
    expected_answer = Answer("test answer")
    mock_langchain_repository.generate_answer.return_value = "test answer"

    # Act
    result = langchain_adapter.generate_answer(user_input, relevant_docs, header)

    # Assert
    mock_langchain_repository.generate_answer.assert_called_once_with(user_input.get_content(), langchain_relevant_docs, header.get_content())
    assert result == expected_answer
