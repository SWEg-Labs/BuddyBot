class CommitFileEntity:
    def __init__(self, filename: str, status: str, changes: int, additions: int, deletions: int, patch: str):
        """
        Inizializza un nuovo oggetto CommitFileEntity, basato su un file coinvolto in un commit di GitHub.

        Args:
            filename (str): Il nome del file.
            status (str): Lo stato del file (ad esempio, "modified", "added", "removed").
            changes (int): Il numero totale di modifiche nel file.
            additions (int): Il numero di righe aggiunte.
            deletions (int): Il numero di righe rimosse.
            patch (str): La patch del file (le modifiche apportate).
        """
        self.filename = filename
        self.status = status
        self.changes = changes
        self.additions = additions
        self.deletions = deletions
        self.patch = patch

    def __repr__(self):
        return f"CommitFileEntity(filename={self.filename}, status={self.status}, changes={self.changes}, additions={self.additions}, deletions={self.deletions}, patch={self.patch})"
    
    def __eq__(self, other):
        if not isinstance(other, CommitFileEntity):
            return False
        return (self.filename == other.filename and
                self.status == other.status and
                self.changes == other.changes and
                self.additions == other.additions and
                self.deletions == other.deletions and
                self.patch == other.patch)
