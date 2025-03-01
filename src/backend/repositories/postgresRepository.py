import psycopg2

from entities.loggingEntities import PostgresLoadingAttempt
from entities.loggingEntities import PostgresPlatformLog
from entities.loggingEntities import PostgresVectorStoreLog
from entities.postgresSaveOperationResponse import PostgresSaveOperationResponse
from utils.logger import logger
from entities.postgresMessage import PostgresMessage

class PostgresRepository:
    '''
    A repository class for interacting with a PostgreSQL database.
    Attributes:
        conn (psycopg2.extensions.connection): The connection object to the PostgreSQL database.
    '''

    def __init__(self, conn: psycopg2.extensions.connection):
        '''
        Initializes the PostgresRepository with the given database connection.
        Args:
            conn (psycopg2.extensions.connection): The connection object to the PostgreSQL database.
        Raises:
            psycopg2.Error: If an error occurs while initializing the PostgresRepository.
        '''
        try:
            self.conn = conn
        except psycopg2.Error as e:
            logger.error(f"An error occurred while initializing the PostgresRepository: {e}")
            self.conn = None

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False) -> tuple | list | None:
        '''
        Initializes the PostgresRepository with the given database connection parameters.
        Executes a given SQL query with optional parameters and fetch options.
        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): The parameters to be used in the SQL query. Defaults to None.
            fetch_one (bool, optional): Whether to fetch a single result. Defaults to False.
            fetch_all (bool, optional): Whether to fetch all results. Defaults to False.
        Returns:
            tuple or list: The fetched result(s) if fetch_one or fetch_all is True, otherwise None.
        Raises:
            psycopg2.Error: If an error occurs while executing the query.
        '''
        try:
            with self.conn.cursor() as cur:  # Cursor creato nel contesto e chiuso automaticamente
                cur.execute(query, params or ())
                if fetch_one:
                    return cur.fetchone()
                if fetch_all:
                    return cur.fetchall()
                self.conn.commit()  # Commit solo per operazioni di scrittura
        except psycopg2.Error as e:
            logger.error(f"An error occurred while executing the query: {e}")
            raise e

    def save_loading_attempt(self, postgres_loading_attempt: PostgresLoadingAttempt) -> PostgresSaveOperationResponse:
        '''
        Saves a loading attempt and its associated logs into the PostgreSQL database.
        Args:
            postgres_loading_attempt (PostgresLoadingAttempt): The loading attempt data to be saved.
        Returns:
            PostgresSaveOperationResponse: The response indicating the success or failure of the save operation.
        Raises:
            psycopg2.Error: If an error occurs while saving the loading attempt in the PostgreSQL database.
        '''
        try:
            create_loading_attempts_table_query = """
            CREATE TABLE IF NOT EXISTS loading_attempts (
                id SERIAL PRIMARY KEY,
                starting_timestamp TIMESTAMP,
                ending_timestamp TIMESTAMP,
                outcome BOOLEAN
            );
            """
            create_platform_logs_table_query = """
            CREATE TABLE IF NOT EXISTS platform_logs (
                id SERIAL PRIMARY KEY,
                loading_attempt_id INTEGER REFERENCES loading_attempts(id),
                loading_item VARCHAR(50),
                timestamp TIMESTAMP,
                outcome BOOLEAN
            );
            """
            create_vector_store_logs_table_query = """
            CREATE TABLE IF NOT EXISTS vector_store_logs (
                id SERIAL PRIMARY KEY,
                loading_attempt_id INTEGER REFERENCES loading_attempts(id),
                timestamp TIMESTAMP,
                outcome BOOLEAN,
                num_added_items INTEGER,
                num_modified_items INTEGER,
                num_deleted_items INTEGER
            );
            """
            insert_loading_attempt_query = """
            INSERT INTO loading_attempts (starting_timestamp, ending_timestamp, outcome)
            VALUES (%s, %s, %s)
            RETURNING id;
            """
            insert_platform_logs_query = """
            INSERT INTO platform_logs (loading_attempt_id, loading_item, timestamp, outcome)
            VALUES (%s, %s, %s, %s);
            """
            insert_vector_store_logs_query = """
            INSERT INTO vector_store_logs (loading_attempt_id, timestamp, outcome, num_added_items, num_modified_items, num_deleted_items)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            
            # Create tables
            self.execute_query(create_loading_attempts_table_query)
            self.execute_query(create_platform_logs_table_query)
            self.execute_query(create_vector_store_logs_table_query)
            
            # Insert loading attempt
            params = (
                postgres_loading_attempt.starting_timestamp,
                postgres_loading_attempt.ending_timestamp,
                postgres_loading_attempt.outcome
            )
            loading_attempt_id = self.execute_query(insert_loading_attempt_query, params=params, fetch_one=True)[0]
            
            # Insert platform logs
            for log in postgres_loading_attempt.postgres_platform_logs:
                self.execute_query(insert_platform_logs_query, params=(loading_attempt_id, log.postgres_loading_items.value, log.timestamp, log.outcome))
            
            # Insert vector store log
            vector_log = postgres_loading_attempt.postgres_vector_store_log
            self.execute_query(insert_vector_store_logs_query, params=(
                loading_attempt_id, vector_log.timestamp, vector_log.outcome, vector_log.num_added_items, vector_log.num_modified_items, vector_log.num_deleted_items
            ))
            
            return PostgresSaveOperationResponse(success=True, message="Loading attempt saved successfully in the Postgres database.")
        
        except psycopg2.Error as e:
            message = f"An error occurred while saving the loading attempt in the Postgres database: {e}"
            logger.error(message)
            return PostgresSaveOperationResponse(success=False, message=message)


    def save_message(self, message: PostgresMessage) -> PostgresSaveOperationResponse:
        '''
        Saves a message into the PostgreSQL database.
        Args:
            message (PostgresMessage): The message data to be saved.
        Returns:
            PostgresSaveOperationResponse: The response indicating the success or failure of the save operation.
        Raises:
            psycopg2.Error: If an error occurs while saving the message in the PostgreSQL database.
        '''
        try:
            create_messages_table_query = """
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                content TEXT,
                timestamp TIMESTAMP,
                sender VARCHAR(50)
            );
            """
            insert_message_query = """
            INSERT INTO messages (content, timestamp, sender)
            VALUES (%s, %s, %s);
            """
            
            # Create table
            self.execute_query(create_messages_table_query)
            
            # Insert message
            params = (message.content, message.timestamp, message.sender.value)
            self.execute_query(insert_message_query, params=params)
            
            return PostgresSaveOperationResponse(success=True, message="Message saved successfully in the Postgres database.")
        
        except psycopg2.Error as e:
            message = f"An error occurred while saving the message in the Postgres database: {e}"
            logger.error(message)
            return PostgresSaveOperationResponse(success=False, message=message)