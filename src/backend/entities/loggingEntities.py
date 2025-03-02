from enum import Enum
from datetime import datetime

class PostgresLoadingItems(Enum):
    GitHubCommits = "GitHubCommits"
    GitHubFiles = "GitHubFiles"
    JiraIssues = "JiraIssues"
    ConfluencePages = "ConfluencePages"

class PostgresPlatformLog:
    def __init__(self, postgres_loading_items: PostgresLoadingItems, timestamp: datetime, outcome: bool):
        self.__postgres_loading_items = postgres_loading_items
        self.__timestamp = timestamp
        self.__outcome = outcome

    def get_postgres_loading_items(self) -> PostgresLoadingItems:
        return self.__postgres_loading_items

    def get_timestamp(self) -> datetime:
        return self.__timestamp

    def get_outcome(self) -> bool:
        return self.__outcome

    def __eq__(self, other):
        if not isinstance(other, PostgresPlatformLog):
            return False
        return (self.__postgres_loading_items == other.get_postgres_loading_items() and
            self.__timestamp == other.get_timestamp() and
            self.__outcome == other.get_outcome())

class PostgresVectorStoreLog:
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

    def __eq__(self, other):
        if not isinstance(other, PostgresVectorStoreLog):
            return False
        return (self.__timestamp == other.get_timestamp() and
            self.__outcome == other.get_outcome() and
            self.__num_added_items == other.get_num_added_items() and
            self.__num_modified_items == other.get_num_modified_items() and
            self.__num_deleted_items == other.get_num_deleted_items())

class PostgresLoadingAttempt:
    def __init__(self, postgres_platform_logs: list[PostgresPlatformLog], postgres_vector_store_log: PostgresVectorStoreLog):
        self.__postgres_platform_logs = postgres_platform_logs
        self.__postgres_vector_store_log = postgres_vector_store_log
        self.__starting_timestamp = postgres_platform_logs[0].get_timestamp()
        self.__ending_timestamp = postgres_vector_store_log.get_timestamp()
        self.__outcome = all(log.get_outcome() for log in postgres_platform_logs) and postgres_vector_store_log.get_outcome()

    def get_postgres_platform_logs(self) -> list[PostgresPlatformLog]:
        return self.__postgres_platform_logs

    def get_postgres_vector_store_log(self) -> PostgresVectorStoreLog:
        return self.__postgres_vector_store_log

    def get_starting_timestamp(self) -> datetime:
        return self.__starting_timestamp

    def get_ending_timestamp(self) -> datetime:
        return self.__ending_timestamp

    def get_outcome(self) -> bool:
        return self.__outcome

    def __eq__(self, other):
        if not isinstance(other, PostgresLoadingAttempt):
            return False
        return (self.__postgres_platform_logs == other.get_postgres_platform_logs() and
            self.__postgres_vector_store_log == other.get_postgres_vector_store_log() and
            self.__starting_timestamp == other.get_starting_timestamp() and
            self.__ending_timestamp == other.get_ending_timestamp() and
            self.__outcome == other.get_outcome())
