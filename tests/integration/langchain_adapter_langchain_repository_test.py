from unittest.mock import MagicMock

from models.document import Document
from models.question import Question
from models.header import Header
from models.answer import Answer
from models.questionAnswerCouple import QuestionAnswerCouple
from models.nextPossibleQuestions import NextPossibleQuestions
from models.possibleQuestion import PossibleQuestion
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


# Verifica che il metodo get_next_possible_questions di LangChainAdapter chiami il metodo get_next_possible_questions di LangChainRepository

def test_get_next_possible_questions_calls_repository_method():
    # Arrange
    max_num_tokens = 128000
    mock_langchain_repository = MagicMock(spec=LangChainRepository)
    langchain_adapter = LangChainAdapter(max_num_tokens, mock_langchain_repository)

    question = Question("test question")
    answer = Answer("test answer")
    question_answer_couple = QuestionAnswerCouple(question, answer)
    header = Header("test header with 3 questions requested")

    expected_repo_couple_parameter = [
        LangChainDocumentEntity(question_answer_couple.get_question().get_content()),
        LangChainDocumentEntity(question_answer_couple.get_answer().get_content())
    ]

    expected_repo_response = (
        "Chi ha risolto la issue BUD-240?___"
        "Cosa ha detto il cliente sulle metriche di qualità?___"
        "Qual è il codice della funzione per prelevare i dati dal database?"
    )
    mock_langchain_repository.get_next_possible_questions.return_value = expected_repo_response

    expected_possible_questions = NextPossibleQuestions(
        num_questions=3,
        possible_questions=[
            PossibleQuestion("Chi ha risolto la issue BUD-240?"),
            PossibleQuestion("Cosa ha detto il cliente sulle metriche di qualità?"),
            PossibleQuestion("Qual è il codice della funzione per prelevare i dati dal database?")
        ]
    )

    # Act
    result = langchain_adapter.get_next_possible_questions(question_answer_couple, header)

    # Assert
    mock_langchain_repository.get_next_possible_questions.assert_called_once_with(
        question_answer_couple = expected_repo_couple_parameter,
        header = header.get_content()
    )
    assert result == expected_possible_questions
