class DocumentEntity:
    def __init__(self, page_content, metadata=None):
        """
        Inizializza un nuovo oggetto DocumentEntity.

        Args:
            page_content (str): Il contenuto del documento.
            metadata (dict, opzionale): Un dizionario contenente i metadati del documento. Default è None.
        """
        self.page_content = page_content
        self.metadata = metadata if metadata is not None else {}

    def __repr__(self):
        return f"DocumentEntity(page_content={self.page_content[:50]}..., metadata={self.metadata})"