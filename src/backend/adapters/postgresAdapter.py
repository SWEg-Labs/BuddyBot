from repositories.postgresRepository import PostgresRepository
from models.dbSaveOperationResponse import DbSaveOperationResponse
from models.loggingModels import LoadingAttempt
from entities.postgresSaveOperationResponse import PostgresSaveOperationResponse
from entities.loggingEntities import PostgresLoadingAttempt, PostgresPlatformLog, PostgresVectorStoreLog, PostgresLoadingItems
from ports.saveLoadingAttemptInDbPort import SaveLoadingAttemptInDbPort
from utils.logger import logger
from models.message import Message, MessageSender
from entities.postgresMessage import PostgresMessage, PostgresMessageSender
from ports.saveMessagePort import SaveMessagePort
from ports.getMessagesPort import GetMessagesPort
from typing import List
from models.quantity import Quantity

class PostgresAdapter(SaveLoadingAttemptInDbPort, SaveMessagePort, GetMessagesPort):
    """
    Adapter class for interacting with a PostgreSQL repository.
    This class provides methods to save loading attempts and convert responses
    between different formats used in the application and the PostgreSQL repository.
    """

    def __init__(self, repository: PostgresRepository):
        """
        Initialize the PostgresAdapter with a given repository.
        Args:
            repository (PostgresRepository): The repository to interact with.
        Raises:
            Exception: If there is an error during initialization.
        """
        try:
            self.__repository = repository
        except Exception as e:
            logger.error(f"Error initializing PostgresAdapter: {e}")

    def save_message(self, message: Message) -> DbSaveOperationResponse:
        """
        Save a message to the PostgreSQL repository.
        Args:
            message (Message): The message to be saved.
        Returns:
            DbSaveOperationResponse: The response from the save operation.
        Raises:
            Exception: If there is an error during the save operation.
        """
        try:
            postgres_message = self.__postgres_message_converter(message)
            postgres_response = self.__repository.save_message(postgres_message)
            return self.__dsor_converter(postgres_response)
        except Exception as e:
            logger.error(f"Error in save_message: {e}")
            return DbSaveOperationResponse(success=False, message=str(e))

    def get_messages(self, quantity: Quantity) -> List[Message]:
        """
        Retrieve a specified quantity of messages.
        Args:
            quantity (Quantity): The number of messages to retrieve.
        Returns:
            List[Message]: A list of retrieved messages.
        Raises:
            Exception: If there is an error during the retrieval operation.
        """
        try:
            postgres_messages = self.__repository.get_messages(quantity.get_value())
            return [self.__message_converter(pm) for pm in postgres_messages]
        except Exception as e:
            logger.error(f"Error in get_messages: {e}")
            raise e
        
    def save_loading_attempt(self, loading_attempt: LoadingAttempt) -> DbSaveOperationResponse:
        """
        Save a loading attempt to the PostgreSQL repository.
        Args:
            loading_attempt (LoadingAttempt): The loading attempt to be saved.
        Returns:
            DbSaveOperationResponse: The response from the save operation.
        Raises:
            Exception: If there is an error during the save operation.
        """
        try:
            postgres_loading_attempt = self.__postgres_loading_attempt_converter(loading_attempt)
            postgres_response = self.__repository.save_loading_attempt(postgres_loading_attempt)
            return self.__dsor_converter(postgres_response)
        except Exception as e:
            logger.error(f"Error in save_loading_attempt: {e}")
            return DbSaveOperationResponse(success=False, message=str(e))
        
    def __dsor_converter(self, psor: PostgresSaveOperationResponse) -> DbSaveOperationResponse:
        """
        Convert a PostgresSaveOperationResponse to a DbSaveOperationResponse.
        Args:
            psor (PostgresSaveOperationResponse): The response from the PostgreSQL repository.
        Returns:
            DbSaveOperationResponse: The converted response.
        Raises:
            Exception: If there is an error during the conversion.
        """
        try:
            return DbSaveOperationResponse(success=psor.get_success(), message=psor.get_message())
        except Exception as e:
            logger.error(f"Error in dsor_converter: {e}")
            return DbSaveOperationResponse(success=False, message=str(e))

    def __postgres_message_converter(self, message: Message) -> PostgresMessage:
        """
        Convert a Message to a PostgresMessage.
        Args:
            message (Message): The message to be converted.
        Returns:
            PostgresMessage: The converted message.
        Raises:
            Exception: If there is an error during the conversion.
        """
        try:
            return PostgresMessage(
                content=message.get_content(),
                timestamp=message.get_timestamp(),
                sender=PostgresMessageSender(message.get_sender().value)
            )
        except Exception as e:
            logger.error(f"Error in postgres_message_converter: {e}")
            raise e
    
    def __message_converter(self, postgres_message: PostgresMessage) -> Message:
        """
        Convert a PostgresMessage to a Message.
        Args:
            postgres_message (PostgresMessage): The message to be converted.
        Returns:
            Message: The converted message.
        Raises:
            Exception: If there is an error during the conversion.
        """
        try:
            return Message(
                content=postgres_message.get_content(),
                timestamp=postgres_message.get_timestamp(),
                sender=MessageSender[postgres_message.get_sender().name]
            )
        except Exception as e:
            logger.error(f"Error in message_converter: {e}")
            raise e
        
    def __postgres_loading_attempt_converter(self, loading_attempt: LoadingAttempt) -> PostgresLoadingAttempt:
        """
        Convert a LoadingAttempt to a PostgresLoadingAttempt.
        Args:
            loading_attempt (LoadingAttempt): The loading attempt to be converted.
        Returns:
            PostgresLoadingAttempt: The converted loading attempt.
        Raises:
            Exception: If there is an error during the conversion.
        """
        try:
            postgres_platform_logs = [
                PostgresPlatformLog(
                    postgres_loading_items=PostgresLoadingItems[log.loading_items.name],
                    timestamp=log.timestamp,
                    outcome=log.outcome
                ) for log in loading_attempt.platform_logs
            ]
            postgres_vector_store_log = PostgresVectorStoreLog(
                timestamp=loading_attempt.vector_store_log.timestamp,
                outcome=loading_attempt.vector_store_log.outcome,
                num_added_items=loading_attempt.vector_store_log.num_added_items,
                num_modified_items=loading_attempt.vector_store_log.num_modified_items,
                num_deleted_items=loading_attempt.vector_store_log.num_deleted_items
            )
            return PostgresLoadingAttempt(
                postgres_platform_logs=postgres_platform_logs,
                postgres_vector_store_log=postgres_vector_store_log
            )
        except Exception as e:
            logger.error(f"Error in postgres_loading_attempt_converter: {e}")
            raise e
