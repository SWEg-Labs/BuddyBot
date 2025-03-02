class IssueEntity:
    def __init__(self, id: str, key: str, summary: str, description: str, issuetype: dict, project: dict, status: dict, priority: dict, assignee: dict, reporter: dict, created: str, updated: str, attachment: list):
        """
        Inizializza un nuovo oggetto IssueEntity, basato su una issue di Jira.

        Args:
            id (str): L'ID dell'issue.
            key (str): La chiave dell'issue.
            summary (str): Un breve riassunto dell'issue.
            description (str): Una descrizione dettagliata dell'issue.
            issuetype (dict): Un dizionario che descrive il tipo di issue.
            project (dict): Un dizionario che descrive il progetto a cui appartiene l'issue.
            status (dict): Un dizionario che descrive lo stato dell'issue.
            priority (dict): Un dizionario che descrive la priorità dell'issue.
            assignee (dict): Un dizionario che descrive la persona assegnata all'issue.
            reporter (dict): Un dizionario che descrive la persona che ha segnalato l'issue.
            created (str): La data e l'ora di creazione dell'issue.
            updated (str): La data e l'ora dell'ultimo aggiornamento dell'issue.
            attachment (list): Una lista di dizionari che descrivono gli allegati dell'issue.
        """
        self.__id = id
        self.__key = key
        self.__summary = summary
        self.__description = description
        self.__issuetype = issuetype
        self.__project = project
        self.__status = status
        self.__priority = priority
        self.__assignee = assignee
        self.__reporter = reporter
        self.__created = created
        self.__updated = updated
        self.__attachment = attachment

    def get_id(self):
        return self.__id

    def get_key(self):
        return self.__key

    def get_summary(self):
        return self.__summary

    def get_description(self):
        return self.__description

    def get_issuetype(self):
        return self.__issuetype

    def get_project(self):
        return self.__project

    def get_status(self):
        return self.__status

    def get_priority(self):
        return self.__priority

    def get_assignee(self):
        return self.__assignee

    def get_reporter(self):
        return self.__reporter

    def get_created(self):
        return self.__created

    def get_updated(self):
        return self.__updated

    def get_attachment(self):
        return self.__attachment

    def __repr__(self):
        return (f"IssueEntity(id={self.__id}, key={self.__key}, summary={self.__summary}, description={self.__description}, "
                f"issuetype={self.__issuetype}, project={self.__project}, status={self.__status}, priority={self.__priority}, "
                f"assignee={self.__assignee}, reporter={self.__reporter}, created={self.__created}, updated={self.__updated}, "
                f"attachment={self.__attachment})")

    def __eq__(self, other):
        if not isinstance(other, IssueEntity):
            return False
        return (self.__id == other.get_id() and
            self.__key == other.get_key() and
            self.__summary == other.get_summary() and
            self.__description == other.get_description() and
            self.__issuetype == other.get_issuetype() and
            self.__project == other.get_project() and
            self.__status == other.get_status() and
            self.__priority == other.get_priority() and
            self.__assignee == other.get_assignee() and
            self.__reporter == other.get_reporter() and
            self.__created == other.get_created() and
            self.__updated == other.get_updated() and
            self.__attachment == other.get_attachment())
