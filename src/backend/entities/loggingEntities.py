from enum import Enum
from datetime import datetime

class PostgresLoadingItems(Enum):
    GitHubCommits = "GitHubCommits"
    GitHubFiles = "GitHubFiles"
    JiraIssues = "JiraIssues"
    ConfluencePages = "ConfluencePages"

class PostgresPlatformLog:
    def __init__(self, postgres_loading_items: PostgresLoadingItems, timestamp: datetime, outcome: bool):
        self.postgres_loading_items = postgres_loading_items
        self.timestamp = timestamp
        self.outcome = outcome

class PostgresVectorStoreLog:
    def __init__(self, timestamp: datetime, outcome: bool, num_added_items: int, num_modified_items: int, num_deleted_items: int):
        self.timestamp = timestamp
        self.outcome = outcome
        self.num_added_items = num_added_items
        self.num_modified_items = num_modified_items
        self.num_deleted_items = num_deleted_items

class PostgresLoadingAttempt:
    def __init__(self, postgres_platform_logs: list[PostgresPlatformLog], postgres_vector_store_log: PostgresVectorStoreLog):
        self.postgres_platform_logs = postgres_platform_logs
        self.postgres_vector_store_log = postgres_vector_store_log
        self.starting_timestamp = postgres_platform_logs[0].timestamp
        self.ending_timestamp = postgres_vector_store_log.timestamp
        self.outcome = all(log.outcome for log in postgres_platform_logs) and postgres_vector_store_log.outcome
