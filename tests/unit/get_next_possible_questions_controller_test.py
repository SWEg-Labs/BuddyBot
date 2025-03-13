import pytest
from unittest.mock import MagicMock

from controllers.getNextPossibleQuestionsController import GetNextPossibleQuestionsController
from use_cases.getNextPossibleQuestionsUseCase import GetNextPossibleQuestionsUseCase


# Verifica che il metodo get_next_possible_questions di GetNextPossibleQuestionsController sollevi un'eccezione se il dizionario 
# ricevuto in input non contiene le chiavi richieste

def test_get_next_possible_questions_missing_keys():
    # Arrange
    mock_use_case = MagicMock(spec=GetNextPossibleQuestionsUseCase)
    controller = GetNextPossibleQuestionsController(mock_use_case)
    invalid_question_answer_quantity = {
        "question": "test question",
        "answer": "test answer"
    }

    # Act
    with pytest.raises(ValueError) as exc_info:
        controller.get_next_possible_questions(invalid_question_answer_quantity)

    # Assert
    assert str(exc_info.value) == "The dictionary must contain 'question', 'answer', and 'quantity' keys."


# Verifica che il metodo get_next_possible_questions di GetNextPossibleQuestionsController sollevi un'eccezione se
# la chiave 'question' del dizionario ricevuto in input non è una stringa

def test_get_next_possible_questions_invalid_question_type():
    # Arrange
    mock_use_case = MagicMock(spec=GetNextPossibleQuestionsUseCase)
    controller = GetNextPossibleQuestionsController(mock_use_case)
    invalid_question_answer_quantity = {
        "question": 123,
        "answer": "test answer",
        "quantity": 3
    }

    # Act
    with pytest.raises(ValueError) as exc_info:
        controller.get_next_possible_questions(invalid_question_answer_quantity)

    # Assert
    assert str(exc_info.value) == "'question' must be a string."


# Verifica che il metodo get_next_possible_questions di GetNextPossibleQuestionsController sollevi un'eccezione se
# la chiave 'answer' del dizionario ricevuto in input non è una stringa

def test_get_next_possible_questions_invalid_answer_type():
    # Arrange
    mock_use_case = MagicMock(spec=GetNextPossibleQuestionsUseCase)
    controller = GetNextPossibleQuestionsController(mock_use_case)
    invalid_question_answer_quantity = {
        "question": "test question",
        "answer": 123,
        "quantity": 3
    }

    # Act
    with pytest.raises(ValueError) as exc_info:
        controller.get_next_possible_questions(invalid_question_answer_quantity)

    # Assert
    assert str(exc_info.value) == "'answer' must be a string."


# Verifica che il metodo get_next_possible_questions di GetNextPossibleQuestionsController sollevi un'eccezione se
# la chiave 'quantity' del dizionario ricevuto in input non è un intero

def test_get_next_possible_questions_invalid_quantity_type():
    # Arrange
    mock_use_case = MagicMock(spec=GetNextPossibleQuestionsUseCase)
    controller = GetNextPossibleQuestionsController(mock_use_case)
    invalid_question_answer_quantity = {
        "question": "test question",
        "answer": "test answer",
        "quantity": "three"
    }

    # Act
    with pytest.raises(ValueError) as exc_info:
        controller.get_next_possible_questions(invalid_question_answer_quantity)

    # Assert
    assert str(exc_info.value) == "'quantity' must be an integer."


# Verifica che il metodo get_next_possible_questions di GetNextPossibleQuestionsController sollevi un'eccezione se,
# nell'oggetto ricevuto da GetNextPossibleQuestionsUseCase, l'attributo del numero di domande non corrisponde alla lunghezza
# dell'attributo lista delle domande possibili

def test_get_next_possible_questions_mismatched_num_questions():
    # Arrange
    mock_use_case = MagicMock(spec=GetNextPossibleQuestionsUseCase)
    controller = GetNextPossibleQuestionsController(mock_use_case)

    question_answer_quantity = {
        "question": "test question",
        "answer": "test answer",
        "quantity": 3
    }

    possible_questions = MagicMock()
    possible_questions.get_num_questions.return_value = 2
    possible_questions.get_possible_questions.return_value = [
        MagicMock(), MagicMock(), MagicMock()
    ]
    mock_use_case.get_next_possible_questions.return_value = possible_questions

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        controller.get_next_possible_questions(question_answer_quantity)
    assert str(exc_info.value) == "The attribute for the number of questions does not match the length of the possible questions list."
