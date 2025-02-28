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
        self.id = id
        self.key = key
        self.summary = summary
        self.description = description
        self.issuetype = issuetype
        self.project = project
        self.status = status
        self.priority = priority
        self.assignee = assignee
        self.reporter = reporter
        self.created = created
        self.updated = updated
        self.attachment = attachment

    def __repr__(self):
        return (f"IssueEntity(id={self.id}, key={self.key}, summary={self.summary}, description={self.description}, "
                f"issuetype={self.issuetype}, project={self.project}, status={self.status}, priority={self.priority}, "
                f"assignee={self.assignee}, reporter={self.reporter}, created={self.created}, updated={self.updated}, "
                f"attachment={self.attachment})")

    def __eq__(self, other):
        if not isinstance(other, IssueEntity):
            return False
        return (self.id == other.id and
                self.key == other.key and
                self.summary == other.summary and
                self.description == other.description and
                self.issuetype == other.issuetype and
                self.project == other.project and
                self.status == other.status and
                self.priority == other.priority and
                self.assignee == other.assignee and
                self.reporter == other.reporter and
                self.created == other.created and
                self.updated == other.updated and
                self.attachment == other.attachment)
