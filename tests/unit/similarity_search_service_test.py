import pytest
from unittest.mock import MagicMock

from models.document import Document
from models.question import Question
from models.documentConstraints import DocumentConstraints
from services.similaritySearchService import SimilaritySearchService
from ports.similaritySearchPort import SimilaritySearchPort


# Verifica che il metodo similarity_search di SimilaritySearchService salti i documenti che superano la soglia di similarità

def test_similarity_search_skips_documents_above_threshold():
    # Arrange
    mock_document_constraints = MagicMock(spec=DocumentConstraints)
    mock_document_constraints.get_similarity_threshold.return_value = 0.6
    mock_document_constraints.get_max_gap.return_value = 0.3
    mock_similarity_search_port = MagicMock(spec=SimilaritySearchPort)
    similarity_search_service = SimilaritySearchService(mock_document_constraints, mock_similarity_search_port)
    user_input = Question("test input")
    documents = [
        Document(page_content="doc1", metadata={"distance": 0.5}),
        Document(page_content="doc2", metadata={"distance": 0.75}),
    ]
    mock_similarity_search_port.similarity_search.return_value = documents

    # Act
    result = similarity_search_service.similarity_search(user_input)

    # Assert
    assert result == [documents[0]]  # Only the first document should be included


# Verifica che il metodo similarity_search di SimilaritySearchService termini e restituisca i documenti trovati finora se il distacco massimo è superato

def test_similarity_search_returns_documents_if_max_gap_exceeded():
    # Arrange
    mock_document_constraints = MagicMock(spec=DocumentConstraints)
    mock_document_constraints.get_similarity_threshold.return_value = 1.2
    mock_document_constraints.get_max_gap.return_value = 0.1
    mock_similarity_search_port = MagicMock(spec=SimilaritySearchPort)
    similarity_search_service = SimilaritySearchService(mock_document_constraints, mock_similarity_search_port)
    user_input = Question("test input")
    documents = [
        Document(page_content="doc1", metadata={"distance": 0.5}),
        Document(page_content="doc2", metadata={"distance": 0.75}),
    ]
    mock_similarity_search_port.similarity_search.return_value = documents

    # Act
    result = similarity_search_service.similarity_search(user_input)

    # Assert
    assert result == [documents[0]]  # Only the first document should be included due to max gap


# Verifica che il metodo similarity_search di SimilaritySearchService gestisca correttamente le eccezioni

def test_similarity_search_handles_exceptions():
    # Arrange
    mock_document_constraints = MagicMock(spec=DocumentConstraints)
    mock_similarity_search_port = MagicMock(spec=SimilaritySearchPort)
    similarity_search_service = SimilaritySearchService(mock_document_constraints, mock_similarity_search_port)
    user_input = Question("test input")
    mock_similarity_search_port.similarity_search.side_effect = Exception("Similarity search error")

    # Act
    with pytest.raises(Exception) as exc_info:
        similarity_search_service.similarity_search(user_input)

    # Assert
    assert str(exc_info.value) == "Similarity search error"
