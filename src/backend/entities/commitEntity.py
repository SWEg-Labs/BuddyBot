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


class CommitEntity:
    def __init__(self, sha: str, message: str, author_name: str, author_email: str, author_date: str, url: str, files: list[CommitFileEntity]):
        """
        Inizializza un nuovo oggetto CommitEntity, basato su un commit di GitHub.

        Args:
            sha (str): La stringa SHA del commit.
            message (str): Il messaggio del commit.
            author_name (str): Il nome dell'autore del commit.
            author_email (str): L'email dell'autore del commit.
            author_date (str): La data del commit.
            url (str): L'URL HTML del commit su GitHub.
            files (list[CommitFileEntity]): Una lista di oggetti CommitFileEntity che rappresentano i file modificati nel commit.
        """
        self.sha = sha
        self.message = message
        self.author_name = author_name
        self.author_email = author_email
        self.author_date = author_date
        self.url = url
        self.files = files

    def __repr__(self):
        return f"CommitEntity(sha={self.sha}, message={self.message}, author_name={self.author_name}, author_email={self.author_email}, author_date={self.author_date}, url={self.url}, files={self.files})"
    
    def __eq__(self, other):
        if not isinstance(other, CommitEntity):
            return False
        return (self.sha == other.sha and
                self.message == other.message and
                self.author_name == other.author_name and
                self.author_email == other.author_email and
                self.author_date == other.author_date and
                self.url == other.url and
                self.files == other.files)
