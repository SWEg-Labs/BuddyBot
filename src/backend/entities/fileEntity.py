class FileEntity:
    def __init__(self, type: str, encoding: str, size: int, name: str, path: str, content: str, sha: str, url: str, html_url: str, download_url: str, git_url: str):
        """
        Inizializza un nuovo oggetto FileEntity, basato su un file di GitHub.

        Args:
            type (str): Il tipo di contenuto, può essere "file" o "dir".
            encoding (str): Il tipo di codifica del contenuto, ad esempio "base64".
            size (int): La dimensione del contenuto in byte.
            name (str): Il nome del file o della directory.
            path (str): Il percorso del file o della directory nel repository.
            content (str): Il contenuto del file codificato (disponibile solo se il tipo è "file").
            sha (str): L'hash SHA del contenuto.
            url (str): L'URL API per accedere al contenuto.
            html_url (str): L'URL HTML per visualizzare il contenuto su GitHub.
            download_url (str): L'URL per scaricare il contenuto.
            git_url (str): L'URL Git per accedere al contenuto.
        """
        self.type = type
        self.encoding = encoding
        self.size = size
        self.name = name
        self.path = path
        self.content = content
        self.sha = sha
        self.url = url
        self.html_url = html_url
        self.download_url = download_url
        self.git_url = git_url

    def __repr__(self):
        return (f"FileEntity(type={self.type}, encoding={self.encoding}, size={self.size}, name={self.name}, "
                f"path={self.path}, content={self.content}, sha={self.sha}, url={self.url}, html_url={self.html_url}, "
                f"download_url={self.download_url}, git_url={self.git_url})")
    
    def __eq__(self, other):
        if not isinstance(other, FileEntity):
            return False
        return (self.type == other.type and
                self.encoding == other.encoding and
                self.size == other.size and
                self.name == other.name and
                self.path == other.path and
                self.content == other.content and
                self.sha == other.sha and
                self.url == other.url and
                self.html_url == other.html_url and
                self.download_url == other.download_url and
                self.git_url == other.git_url)
