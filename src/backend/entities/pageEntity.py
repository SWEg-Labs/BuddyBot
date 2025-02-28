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
        self.id = id
        self.type = type
        self.title = title
        self.space = space
        self.body = body
        self.version = version
        self.status = status
        self.ancestors = ancestors
        self.extensions = extensions
        self.links = links

    def __repr__(self):
        return (f"PageEntity(id={self.id}, type={self.type}, title={self.title}, space={self.space}, "
                f"body={self.body}, version={self.version}, status={self.status}, ancestors={self.ancestors}, "
                f"extensions={self.extensions}, links={self.links})")

    def __eq__(self, other):
        if not isinstance(other, PageEntity):
            return False
        return (self.id == other.id and
                self.type == other.type and
                self.title == other.title and
                self.space == other.space and
                self.body == other.body and
                self.version == other.version and
                self.status == other.status and
                self.ancestors == other.ancestors and
                self.extensions == other.extensions and
                self.links == other.links)
