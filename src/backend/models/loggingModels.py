from enum import Enum
from datetime import datetime

class LoadingItems(Enum):
    GitHubCommits = "GitHub Commits"
    GitHubFiles = "GitHub Files"
    JiraIssues = "Jira Issues"
    ConfluencePages = "Confluence Pages"

class PlatformLog:
    def __init__(self, loading_items: LoadingItems, timestamp: datetime, outcome: bool):
        self.__loading_items = loading_items
        self.__timestamp = timestamp
        self.__outcome = outcome

    def get_loading_items(self) -> LoadingItems:
        return self.__loading_items

    def get_timestamp(self) -> datetime:
        return self.__timestamp

    def get_outcome(self) -> bool:
        return self.__outcome

    def __eq__(self, other) -> bool:
        if not isinstance(other, PlatformLog):
            return False
        return (self.__loading_items == other.get_loading_items() and
            self.__timestamp == other.get_timestamp() and
            self.__outcome == other.get_outcome())

class VectorStoreLog:
    def __init__(self, timestamp: datetime, outcome: bool, num_added_items: int, num_modified_items: int, num_deleted_items: int):
        self.__timestamp = timestamp
        self.__outcome = outcome
        self.__num_added_items = num_added_items
        self.__num_modified_items = num_modified_items
        self.__num_deleted_items = num_deleted_items

    def get_timestamp(self) -> datetime:
        return self.__timestamp

    def get_outcome(self) -> bool:
        return self.__outcome

    def get_num_added_items(self) -> int:
        return self.__num_added_items

    def get_num_modified_items(self) -> int:
        return self.__num_modified_items

    def get_num_deleted_items(self) -> int:
        return self.__num_deleted_items

    def __eq__(self, other) -> bool:
        if not isinstance(other, VectorStoreLog):
            return False
        return (self.__timestamp == other.get_timestamp() and
            self.__outcome == other.get_outcome() and
            self.__num_added_items == other.get_num_added_items() and
            self.__num_modified_items == other.get_num_modified_items() and
            self.__num_deleted_items == other.get_num_deleted_items())

class LoadingAttempt:
    def __init__(self, platform_logs: list[PlatformLog], vector_store_log: VectorStoreLog, starting_timestamp: datetime):
        self.__platform_logs = platform_logs
        self.__vector_store_log = vector_store_log
        self.__starting_timestamp = starting_timestamp
        self.__ending_timestamp = vector_store_log.get_timestamp()
        self.__outcome = all(log.get_outcome() for log in platform_logs) and vector_store_log.get_outcome()

    def get_platform_logs(self) -> list[PlatformLog]:
        return self.__platform_logs

    def get_vector_store_log(self) -> VectorStoreLog:
        return self.__vector_store_log

    def get_starting_timestamp(self) -> datetime:
        return self.__starting_timestamp

    def get_ending_timestamp(self) -> datetime:
        return self.__ending_timestamp

    def get_outcome(self) -> bool:
        return self.__outcome

    def __eq__(self, other) -> bool:
        if not isinstance(other, LoadingAttempt):
            return False
        return (self.__platform_logs == other.get_platform_logs() and
            self.__vector_store_log == other.get_vector_store_log() and
            self.__starting_timestamp == other.get_starting_timestamp() and
            self.__ending_timestamp == other.get_ending_timestamp() and
            self.__outcome == other.get_outcome())
