from enum import Enum
from datetime import datetime

class LoadingItems(Enum):
    GitHubCommits = "GitHubCommits"
    GitHubFiles = "GitHubFiles"
    JiraIssues = "JiraIssues"
    ConfluencePages = "ConfluencePages"

class PlatformLog:
    def __init__(self, loading_items: LoadingItems, timestamp: datetime, outcome: bool):
        self.loading_items = loading_items
        self.timestamp = timestamp
        self.outcome = outcome

    def __eq__(self, other):
        if not isinstance(other, PlatformLog):
            return False
        return (self.loading_items == other.loading_items and
                self.timestamp == other.timestamp and
                self.outcome == other.outcome)

class VectorStoreLog:
    def __init__(self, timestamp: datetime, outcome: bool, num_added_items: int, num_modified_items: int, num_deleted_items: int):
        self.timestamp = timestamp
        self.outcome = outcome
        self.num_added_items = num_added_items
        self.num_modified_items = num_modified_items
        self.num_deleted_items = num_deleted_items

    def __eq__(self, other):
        if not isinstance(other, VectorStoreLog):
            return False
        return (self.timestamp == other.timestamp and
                self.outcome == other.outcome and
                self.num_added_items == other.num_added_items and
                self.num_modified_items == other.num_modified_items and
                self.num_deleted_items == other.num_deleted_items)

class LoadingAttempt:
    def __init__(self, platform_logs: list[PlatformLog], vector_store_log: VectorStoreLog):
        self.platform_logs = platform_logs
        self.vector_store_log = vector_store_log
        self.starting_timestamp = platform_logs[0].timestamp
        self.ending_timestamp = vector_store_log.timestamp
        self.outcome = all(log.outcome for log in platform_logs) and vector_store_log.outcome

    def __eq__(self, other):
        if not isinstance(other, LoadingAttempt):
            return False
        return (self.platform_logs == other.platform_logs and
                self.vector_store_log == other.vector_store_log and
                self.starting_timestamp == other.starting_timestamp and
                self.ending_timestamp == other.ending_timestamp and
                self.outcome == other.outcome)
