from unittest.mock import MagicMock
from models.document import Document
from models.question import Question
from entities.queryResultEntity import QueryResultEntity
from adapters.chromaVectorStoreAdapter import ChromaVectorStoreAdapter
from repositories.chromaVectorStoreRepository import ChromaVectorStoreRepository

# Verifica che il metodo similarity_search di ChromaVectorStoreAdapter chiami il metodo similarity_search di ChromaVectorStoreRepository

def test_similarity_search_calls_repository():
    # Arrange
    mock_repository = MagicMock(spec=ChromaVectorStoreRepository)
    adapter = ChromaVectorStoreAdapter(mock_repository)
    user_input = Question("test query")
    documents = [
        Document(page_content="doc1", metadata={"author": "Author1", "distance": 0.5}),
        Document(page_content="doc2", metadata={"author": "Author2", "distance": 0.75}),
    ]
    query_result_entity = QueryResultEntity(
        documents=[["doc1", "doc2"]],
        metadatas=[[{"author": "Author1"}, {"author": "Author2"}]],
        distances=[[0.5, 0.75]],
    )
    mock_repository.similarity_search.return_value = query_result_entity

    # Act
    result = adapter.similarity_search(user_input)

    # Assert
    mock_repository.similarity_search.assert_called_once_with(user_input.content)
    assert result == documents
