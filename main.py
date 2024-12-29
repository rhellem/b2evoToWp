import logging

from myCommons.modules.envMgr import EnvSetupManager
from myCommons.modules.configReader import ConfigReader
from modules.db.connectionManager import connectionManager

logger = None
b2evo_config = None
wp_config = None
b2Connection = None
wpConnection = None

def configure_logging():
    """
    Configure the logging system to be used across all modules.
    This sets up both file-based and console-based logging with appropriate formats.
    """
    # Define custom format for logs
    log_format = '%(asctime)s - %(levelname)s - %(threadName)s - %(module)s - %(funcName)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    # Configure logging globally
    logging.basicConfig(
        level=logging.INFO,  # Set the default logging level
        format=log_format,   # Log message format
        datefmt=date_format, # Date format
        handlers=[
            # Log to a file
            logging.FileHandler('application-debug.log', mode='w'),
            # Log to the console
            logging.StreamHandler()
        ]
    )

    # Log a simple message to confirm configuration
    logging.info("Logging is configured and ready.")    
    global logger
    logger = logging.getLogger(__name__)  # Obtain the logger for this module
        
def loadConfig():
    
    logger.info("Load the databaseconfig")
    config_reader = ConfigReader("db_config.yaml")
    
    try:
        global b2evo_config 
        b2evo_config = config_reader.get_database_config("b2evolution")
        
        logger.info("Database Config: %s", b2evo_config)
        global wp_config 
        wp_config = config_reader.get_database_config("wordpress")
        
        logger.info("Database Config: %s", wp_config)
        
    except (FileNotFoundError, ValueError) as e:
        logger.error(e)

def connectToDatabases():
    logger.info("About to open connections the source and target database")
    
    myDatabaseManager = connectionManager()
    global b2Connection
    b2Connection = myDatabaseManager.connect_to_database(b2evo_config)
    global wpConnection
    wpConnection = myDatabaseManager.connect_to_database(wp_config)

    
def main():
    configure_logging()
    
    logger.info("Create the virtual environment, download requirements")
    # Fix all related to pip and requirements
    envManager = EnvSetupManager()
    envManager.setup_environment()
    
    # Load the database config
    loadConfig()
 
    # Connect to the databases
    connectToDatabases()
    
    b2Connection.close()

if __name__ == "__main__":
    main()