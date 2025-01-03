import logging
import sys

import mysql
from mysql.connector import Error
from myCommons.modules.configReader import ConfigReader

logger = logging.getLogger(__name__)


class connectionManager:
    """Database Helper class"""
    def __init__(self):
      pass
      
    
    def connect_to_database(self, config: ConfigReader):
        """
        Establish a connection to the MySQL database using the given configuration.

        :param config: Dictionary containing database connection parameters (host, user, password).
        :return: A MySQL connection object if successful, or None if an error occurs.
        """
        try:
            # Validate required configuration fields
            required_keys = ["host", "user", "password"]
            for key in required_keys:
                if key not in config:
                    raise KeyError(f"Missing required configuration key: '{key}'")

            # Attempt to connect to the database
            connection = mysql.connector.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"],
                database=config["name"]
            )
            
            # Check if the connection was successful
            if connection.is_connected():
                logger.info("Successfully connected to the database %s", config["name"])
                return connection

        except KeyError as e:
            logger.error("Configuration error: %s", e)
            sys.exit(e)
        except Error as e:
            logger.error("Database Connection Error: %s", e)
            sys.exit(e)
        except Exception as e:
            logger.error("An unexptected error occured: %s", e)
            sys.exit(e)
        # Return None if the connection fails
        logger.warning("No connection, return None")
        return None