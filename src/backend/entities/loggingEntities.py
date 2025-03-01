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

    def __eq__(self, other):
        if not isinstance(other, PostgresPlatformLog):
            return False
        return (self.postgres_loading_items == other.postgres_loading_items and
                self.timestamp == other.timestamp and
                self.outcome == other.outcome)

class PostgresVectorStoreLog:
    def __init__(self, timestamp: datetime, outcome: bool, num_added_items: int, num_modified_items: int, num_deleted_items: int):
        self.timestamp = timestamp
        self.outcome = outcome
        self.num_added_items = num_added_items
        self.num_modified_items = num_modified_items
        self.num_deleted_items = num_deleted_items

    def __eq__(self, other):
        if not isinstance(other, PostgresVectorStoreLog):
            return False
        return (self.timestamp == other.timestamp and
                self.outcome == other.outcome and
                self.num_added_items == other.num_added_items and
                self.num_modified_items == other.num_modified_items and
                self.num_deleted_items == other.num_deleted_items)

class PostgresLoadingAttempt:
    def __init__(self, postgres_platform_logs: list[PostgresPlatformLog], postgres_vector_store_log: PostgresVectorStoreLog):
        self.postgres_platform_logs = postgres_platform_logs
        self.postgres_vector_store_log = postgres_vector_store_log
        self.starting_timestamp = postgres_platform_logs[0].timestamp
        self.ending_timestamp = postgres_vector_store_log.timestamp
        self.outcome = all(log.outcome for log in postgres_platform_logs) and postgres_vector_store_log.outcome

    def __eq__(self, other):
        if not isinstance(other, PostgresLoadingAttempt):
            return False
        return (self.postgres_platform_logs == other.postgres_platform_logs and
                self.postgres_vector_store_log == other.postgres_vector_store_log and
                self.starting_timestamp == other.starting_timestamp and
                self.ending_timestamp == other.ending_timestamp and
                self.outcome == other.outcome)