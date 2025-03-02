class PageEntity:
    def __init__(self, id: str, type: str, title: str, space: dict, body: dict, version: dict, status: str, ancestors: list, extensions: dict, links: dict):
        """
        Inizializza un nuovo oggetto PageEntity, basato su una pagina di Confluence.

        Args:
            id (str): L'ID della pagina.
            type (str): Il tipo di contenuto, in questo caso "page".
            title (str): Il titolo della pagina.
            space (dict): Un dizionario che descrive lo spazio a cui appartiene la pagina.
            body (dict): Un dizionario che contiene il contenuto della pagina.
            version (dict): Un dizionario che descrive la versione della pagina.
            status (str): Lo stato della pagina.
            ancestors (list): Una lista di dizionari che descrivono gli antenati della pagina.
            extensions (dict): Un dizionario che contiene estensioni specifiche della pagina.
            links (dict): Un dizionario che contiene i link relativi alla pagina.
        """
        self.__id = id
        self.__type = type
        self.__title = title
        self.__space = space
        self.__body = body
        self.__version = version
        self.__status = status
        self.__ancestors = ancestors
        self.__extensions = extensions
        self.__links = links

    def get_id(self) -> str:
        return self.__id

    def get_type(self) -> str:
        return self.__type

    def get_title(self) -> str:
        return self.__title

    def get_space(self) -> dict:
        return self.__space

    def get_body(self) -> dict:
        return self.__body

    def get_version(self) -> dict:
        return self.__version

    def get_status(self) -> str:
        return self.__status

    def get_ancestors(self) -> list:
        return self.__ancestors

    def get_extensions(self) -> dict:
        return self.__extensions

    def get_links(self) -> dict:
        return self.__links

    def __repr__(self):
        return (f"PageEntity(id={self.__id}, type={self.__type}, title={self.__title}, space={self.__space}, "
                f"body={self.__body}, version={self.__version}, status={self.__status}, ancestors={self.__ancestors}, "
                f"extensions={self.__extensions}, links={self.__links})")

    def __eq__(self, other):
        if not isinstance(other, PageEntity):
            return False
        return (self.__id == other.get_id() and
            self.__type == other.get_type() and
            self.__title == other.get_title() and
            self.__space == other.get_space() and
            self.__body == other.get_body() and
            self.__version == other.get_version() and
            self.__status == other.get_status() and
            self.__ancestors == other.get_ancestors() and
            self.__extensions == other.get_extensions() and
            self.__links == other.get_links())
