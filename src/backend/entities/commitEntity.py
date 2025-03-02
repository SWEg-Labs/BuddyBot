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
        self.__filename = filename
        self.__status = status
        self.__changes = changes
        self.__additions = additions
        self.__deletions = deletions
        self.__patch = patch

    def get_filename(self):
        return self.__filename

    def get_status(self):
        return self.__status

    def get_changes(self):
        return self.__changes

    def get_additions(self):
        return self.__additions

    def get_deletions(self):
        return self.__deletions

    def get_patch(self):
        return self.__patch

    def __repr__(self):
        return f"CommitFileEntity(filename={self.__filename}, status={self.__status}, changes={self.__changes}, additions={self.__additions}, deletions={self.__deletions}, patch={self.__patch})"
    
    def __eq__(self, other):
        if not isinstance(other, CommitFileEntity):
            return False
        return (self.get_filename() == other.get_filename() and
            self.get_status() == other.get_status() and
            self.get_changes() == other.get_changes() and
            self.get_additions() == other.get_additions() and
            self.get_deletions() == other.get_deletions() and
            self.get_patch() == other.get_patch())


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
        self.__sha = sha
        self.__message = message
        self.__author_name = author_name
        self.__author_email = author_email
        self.__author_date = author_date
        self.__url = url
        self.__files = files

    def get_sha(self):
        return self.__sha

    def get_message(self):
        return self.__message

    def get_author_name(self):
        return self.__author_name

    def get_author_email(self):
        return self.__author_email

    def get_author_date(self):
        return self.__author_date

    def get_url(self):
        return self.__url

    def get_files(self):
        return self.__files

    def __repr__(self):
        return f"CommitEntity(sha={self.__sha}, message={self.__message}, author_name={self.__author_name}, author_email={self.__author_email}, author_date={self.__author_date}, url={self.__url}, files={self.__files})"
    
    def __eq__(self, other):
        if not isinstance(other, CommitEntity):
            return False
        return (self.get_sha() == other.get_sha() and
            self.get_message() == other.get_message() and
            self.get_author_name() == other.get_author_name() and
            self.get_author_email() == other.get_author_email() and
            self.get_author_date() == other.get_author_date() and
            self.get_url() == other.get_url() and
            self.get_files() == other.get_files())
