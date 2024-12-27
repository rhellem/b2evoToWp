import logging

from myCommons.modules.envMgr import EnvSetupManager
from myCommons.modules.configReader import ConfigReader

logger = None

def configureLogging():
    # Set up a basic logger
    global logger
    logger = logging.getLogger(__name__)

    filehandler_dbg = logging.FileHandler(logger.name + '-debug.log', mode='w')
    #Create custom formats of the logrecord fit for both the logfile and the console
    streamformatter = logging.Formatter(fmt='%(levelname)s:\t%(threadName)s:\t%(funcName)s:\t\t%(message)s', datefmt='%H:%M:%S') #We only want to see certain parts of the message


    #Apply formatters to handlers
    filehandler_dbg.setFormatter(streamformatter)


    #Add handlers to logger
    logger.addHandler(filehandler_dbg)
    
    
    logger.setLevel(logging.INFO)

    # Create a handler to output logs to the console
    console_handler = logging.StreamHandler()

    # Define a basic formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Add the formatter to the handler
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    # Log a simple message
    logger.info("Logging is now ready")
    

        
def loadConfig():
    
    logger.info("Load the databaseconfig")
    config_reader = ConfigReader("db_config.yaml")
    
    try:
        b2evo_config = config_reader.get_database_config("b2evolution")
        
        logger.info("Database Config: %s", b2evo_config)
        wp_config = config_reader.get_database_config("wordpress")
        
        logger.info("Database Config: %s", wp_config)
    except (FileNotFoundError, ValueError) as e:
        logger.error(e)


    
def main():
    configureLogging()
    logger.info("Create the virtual environment, download requirements")
    # Fix all related to pip and requirements
    envManager = EnvSetupManager()
    envManager.setup_environment()
    
    # Load the database config
    loadConfig()
 
    
    

if __name__ == "__main__":
    main()