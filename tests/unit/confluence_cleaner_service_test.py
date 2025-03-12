import pytest

from models.document import Document
from services.confluenceCleanerService import ConfluenceCleanerService


# Verifica che il metodo clean_confluence_pages di ConfluenceCleanerService pulisca correttamente le pagine Confluence

def test_clean_confluence_pages():
    # Arrange
    service = ConfluenceCleanerService()
    pages = [
        Document(page_content="<html>doc1 &agrave; &egrave; &igrave; &ograve; &ugrave; &quot; &Egrave;</html>", metadata={"id": 1}),
        Document(page_content="<html>doc2 &agrave; &egrave; &igrave; &ograve; &ugrave; &quot; &Egrave;</html>", metadata={"id": 2}),
    ]
    expected_cleaned_pages = [
        Document(page_content=" doc1 à è ì ò ù \" È ", metadata={"id": 1}),
        Document(page_content=" doc2 à è ì ò ù \" È ", metadata={"id": 2}),
    ]

    # Act
    result = service.clean_confluence_pages(pages)

    # Assert
    assert result == expected_cleaned_pages


# Verifica che il metodo clean_confluence_pages di ConfluenceCleanerService gestisca correttamente le eccezioni

def test_clean_confluence_pages_exception():
    # Arrange
    service = ConfluenceCleanerService()
    pages = [Document(page_content="", metadata={"id": 1})]  # Empty content to trigger ValueError

    # Act
    with pytest.raises(ValueError) as exc_info:
        service.clean_confluence_pages(pages)

    # Assert
    assert str(exc_info.value) == "Document content is empty"


# Verifica che il metodo remove_html_tags di ConfluenceCleanerService rimuova correttamente i tag HTML
def test_remove_html_tags():
    # Arrange
    service = ConfluenceCleanerService()
    document = Document(page_content="<html>doc1</html>", metadata={"id": 1})
    expected_document = Document(page_content=" doc1 ", metadata={"id": 1})

    # Act
    result = service._ConfluenceCleanerService__remove_html_tags(document)

    # Assert
    assert result == expected_document


# Verifica che il metodo remove_html_tags di ConfluenceCleanerService gestisca correttamente le eccezioni

def test_remove_html_tags_exception():
    # Arrange
    service = ConfluenceCleanerService()
    document = Document(page_content="", metadata={"id": 1})  # Empty content to trigger ValueError

    # Act
    with pytest.raises(ValueError) as exc_info:
        service._ConfluenceCleanerService__remove_html_tags(document)

    # Assert
    assert str(exc_info.value) == "Document content is empty"


# Verifica che il metodo replace_html_entities di ConfluenceCleanerService sostituisca correttamente le entità HTML

def test_replace_html_entities():
    # Arrange
    service = ConfluenceCleanerService()
    document = Document(page_content="&agrave; &egrave; &igrave; &ograve; &ugrave; &quot; &Egrave;", metadata={"id": 1})
    expected_document = Document(page_content="à è ì ò ù \" È", metadata={"id": 1})

    # Act
    result = service._ConfluenceCleanerService__replace_html_entities(document)

    # Assert
    assert result == expected_document


# Verifica che il metodo replace_html_entities di ConfluenceCleanerService gestisca correttamente le eccezioni

def test_replace_html_entities_exception():
    # Arrange
    service = ConfluenceCleanerService()
    document = Document(page_content="", metadata={"id": 1})  # Empty content to trigger ValueError

    # Act
    with pytest.raises(ValueError) as exc_info:
        service._ConfluenceCleanerService__replace_html_entities(document)

    # Assert
    assert str(exc_info.value) == "Document content is empty"
