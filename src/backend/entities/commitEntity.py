class CommitEntity:
    def __init__(self, sha, message, author_name, author_email, author_date, url, files=None):
        """
        Inizializza un nuovo oggetto CommitEntity, basato su un commit di GitHub.

        Args:
            sha (str): La stringa SHA del commit.
            message (str): Il messaggio del commit.
            author_name (str): Il nome dell'autore del commit.
            author_email (str): L'email dell'autore del commit.
            author_date (str): La data del commit.
            url (str): L'URL HTML del commit su GitHub.
            files (list, opzionale): Una lista di oggetti File che rappresentano i file modificati nel commit. Default è None.
        """
        self.sha = sha
        self.message = message
        self.author_name = author_name
        self.author_email = author_email
        self.author_date = author_date
        self.url = url
        self.files = files if files is not None else []

    def __repr__(self):
        return f"Commit(sha={self.sha}, message={self.message}, author_name={self.author_name}, author_email={self.author_email}, author_date={self.author_date}, url={self.url}, files={self.files})"
    
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
