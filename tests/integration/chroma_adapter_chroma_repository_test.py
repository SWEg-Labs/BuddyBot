from unittest.mock import MagicMock
from datetime import datetime
import pytz
from freezegun import freeze_time

from models.document import Document
from models.question import Question
from models.loggingModels import VectorStoreLog
from entities.queryResultEntity import QueryResultEntity
from entities.chromaDocumentEntity import ChromaDocumentEntity
from adapters.chromaVectorStoreAdapter import ChromaVectorStoreAdapter
from repositories.chromaVectorStoreRepository import ChromaVectorStoreRepository


# Verifica che il metodo similarity_search di ChromaVectorStoreAdapter chiami il metodo similarity_search di ChromaVectorStoreRepository

def test_similarity_search_calls_repository():
    # Arrange
    mock_repository = MagicMock(spec=ChromaVectorStoreRepository)
    max_chunk_size = 41666
    adapter = ChromaVectorStoreAdapter(max_chunk_size, mock_repository)
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
    mock_repository.similarity_search.assert_called_once_with(user_input.get_content())
    assert result == documents


# Verifica che il metodo load di ChromaVectorStoreAdapter chiami il metodo load di ChromaVectorStoreRepository

@freeze_time("2025-03-01 12:00:00")  # Freeze time to avoid issues with datetime.now(italy_tz)
def test_load_calls_repository():
    # Arrange
    mock_repository = MagicMock(spec=ChromaVectorStoreRepository)
    max_chunk_size = 41666
    adapter = ChromaVectorStoreAdapter(max_chunk_size, mock_repository)
    documents = [
        Document(page_content="doc1", metadata={"author": "Author1", "id": "1"}),
        Document(page_content="doc2", metadata={"author": "Author2", "id": "2"}),
    ]
    italy_tz = pytz.timezone('Europe/Rome')
    document_entities = [
        ChromaDocumentEntity(page_content="doc1",
                       metadata={"author": "Author1", "id": "1", "chunk_index": 0, "doc_id": "1_0", "vector_store_insertion_date": datetime.now(italy_tz).strftime("%Y-%m-%dT%H:%M:%S")}),
        ChromaDocumentEntity(page_content="doc2",
                       metadata={"author": "Author2", "id": "2", "chunk_index": 0, "doc_id": "2_0", "vector_store_insertion_date": datetime.now(italy_tz).strftime("%Y-%m-%dT%H:%M:%S")}),
    ]

    vector_store_log = VectorStoreLog(
        timestamp=datetime(2025, 2, 28, 12, 34, 56),
        outcome=True,
        num_added_items=4,
        num_modified_items=0,
        num_deleted_items=0,
    )
    mock_repository.load.return_value = vector_store_log

    # Act
    result = adapter.load(documents)

    # Assert
    mock_repository.load.assert_called_once_with(document_entities)
    assert result == vector_store_log
