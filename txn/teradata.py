import teradatasql
import time
import pandas as pd
import logging


# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class TeradataConnectionManager:
    def __init__(self, host, user, password):
        """
        Initialize the TeradataConnectionManager with connection details.
        
        :param host: Teradata server host
        :param user: Username for the Teradata connection
        :param password: Password for the Teradata connection
        """
        self.host = host
        self.user = user
        self.password = password
        self.connection = None
        self.last_checked = None
        self.connection_timeout = 300  # Timeout in seconds (e.g., 5 minutes)

    def get_connection(self):
        """
        Get a valid connection to Teradata. If no connection exists, or the 
        existing connection is inactive or stale, create a new connection.
        
        :return: Active Teradata connection
        """
        if self.connection and self._is_connection_active():
            logger.info("Reusing an active Teradata connection.")
            return self.connection

        # If no valid connection, create a new one
        self._create_new_connection()
        return self.connection

    def _is_connection_active(self):
        """
        Check if the existing connection is active and not stale.
        
        :return: True if connection is active, False otherwise
        """
        # Check if the connection is alive
        try:
            if self.connection:
                self.connection.cursor().execute("SELECT 1")
                if time.time() - self.last_checked > self.connection_timeout:
                    logger.warning("The connection is stale. Reinitializing...")
                    return False
                return True
        except Exception as e:
            logger.error(f"Connection check failed: {e}")
            return False
        return False

    def _create_new_connection(self):
        """
        Create a new connection to the Teradata database.
        """
        if self.connection:
            try:
                self.connection.close()
                logger.info("Closed the existing stale connection.")
            except Exception as e:
                logger.error(f"Error closing the stale connection: {e}")

        try:
            self.connection = teradatasql.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            self.last_checked = time.time()
            logger.info("New Teradata connection established successfully.")
        except Exception as e:
            logger.error(f"Failed to establish a new connection: {e}")
            raise

    def get(self, sql):
        """
        Execute a SQL query and return the result as a pandas DataFrame.
        
        :param sql: The SQL query to execute
        :return: pandas DataFrame containing the query result
        """
        connection = self.get_connection()
        try:
            logger.info(f"Executing query: {sql}")
            # Use pandas to read the SQL query and return the result as a DataFrame
            df = pd.read_sql(sql, connection)
            logger.info("Query executed successfully.")
            return df
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise


# Example usage:
if __name__ == "__main__":
    # Replace with your actual Teradata credentials
    HOST = "your_teradata_host"
    USER = "your_username"
    PASSWORD = "your_password"

    manager = TeradataConnectionManager(HOST, USER, PASSWORD)

    # Example SQL query
    sql_query = "SELECT TOP 10 * FROM your_table_name"

    try:
        # Fetch the query result as a DataFrame
        df = manager.get(sql_query)
        print(df)
    except Exception as e:
        logger.error(f"Error: {e}")
