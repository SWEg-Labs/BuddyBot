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
        self.__type = type
        self.__encoding = encoding
        self.__size = size
        self.__name = name
        self.__path = path
        self.__content = content
        self.__sha = sha
        self.__url = url
        self.__html_url = html_url
        self.__download_url = download_url
        self.__git_url = git_url

    def get_type(self) -> str:
        return self.__type

    def get_encoding(self) -> str:
        return self.__encoding

    def get_size(self) -> int:
        return self.__size

    def get_name(self) -> str:
        return self.__name

    def get_path(self) -> str:
        return self.__path

    def get_content(self) -> str:
        return self.__content

    def get_sha(self) -> str:
        return self.__sha

    def get_url(self) -> str:
        return self.__url

    def get_html_url(self) -> str:
        return self.__html_url

    def get_download_url(self) -> str:
        return self.__download_url

    def get_git_url(self) -> str:
        return self.__git_url

    def __repr__(self):
        return (f"FileEntity(type={self.__type}, encoding={self.__encoding}, size={self.__size}, name={self.__name}, "
                f"path={self.__path}, content={self.__content}, sha={self.__sha}, url={self.__url}, html_url={self.__html_url}, "
                f"download_url={self.__download_url}, git_url={self.__git_url})")
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, FileEntity):
            return False
        return (self.__type == other.get_type() and
            self.__encoding == other.get_encoding() and
            self.__size == other.get_size() and
            self.__name == other.get_name() and
            self.__path == other.get_path() and
            self.__content == other.get_content() and
            self.__sha == other.get_sha() and
            self.__url == other.get_url() and
            self.__html_url == other.get_html_url() and
            self.__download_url == other.get_download_url() and
            self.__git_url == other.get_git_url())
