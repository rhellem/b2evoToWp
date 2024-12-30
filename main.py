import logging
import sys
import mysql

from modules.conversionHelper import ConversionHelper
from myCommons.modules.envMgr import EnvSetupManager
from myCommons.modules.configReader import ConfigReader
from modules.db.connectionManager import connectionManager
from modules.db.wpQueryHelper import wpQueryHelper


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
        level=logging.DEBUG,  # Set the default logging level
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

def doBlogs():
    """    
    Import all blog instances from B2Evolution, making them the top categories in Wordpress
    This since WP does not have the concept of multiple blogs, which enables you to individually apply access controll 
    But, WP can do this pr. main categories
    """
    logger.info("Query for all blogs found in b2Evolution")
    b2e_blogs_query = wpQueryHelper.getSelectB2AllBlogs()
    # https://stackoverflow.com/a/75691255/512139
    b2MySqlCursor = b2Connection.cursor(dictionary=True)
    b2MySqlCursor.execute(b2e_blogs_query)
    allBlogsResult = b2MySqlCursor.fetchall()
    
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        for row in allBlogsResult:
            logger.debug("%s",row)
    
    if allBlogsResult is None:
        logger.error("No blogs found, exit")
        sys.exit("No blogs found")
    else:
        # Get all blogs from b2 and add as main categories in WP
        wpMySqlCursor = wpConnection.cursor()
        # Query to insert each main category
        wp_terms_insert = wpQueryHelper.getInsertMainCatetgories()
        wp_terms_taxonomy_insert = wpQueryHelper.getInsertWpTermTaxonomy()
        for row in allBlogsResult:
            slug = ConversionHelper.sanitize_title(row["blog_shortname"])
            logger.debug("slug=%s", slug)
            
            mainCategoryValues = (row["blog_id"], row["blog_name"], slug)
            logger.debug("Now insert into wp the main categories: %s", mainCategoryValues)
            wpMySqlCursor.execute(wp_terms_insert, mainCategoryValues)
            
            try:
                # Get the term_id for each category and insert these into the wp_term_taxonomy table:
                mainCategoryTaxonomyValues = (row["blog_id"],'category',row["blog_name"],0)
                logger.debug("Now insert into wp_term_taxonomy: %s", mainCategoryTaxonomyValues)
                wpMySqlCursor.execute(wp_terms_taxonomy_insert, mainCategoryTaxonomyValues)
            except mysql.connector.errors.IntegrityError as e:
                logger.warning("IntegrityError occurred: %s. Continuing execution.", e)

        logger.info("Now commit main categories to WP")
        wpConnection.commit()
        
        
        
        
        
        
def doCategories():
    """
    Import all categories from B2Evolution, making them subcategories of the main categories in Wordpress
    Pr blog, get all categories belonging to that blog which does not have a parent category.
    Then insert these as subcategories to the main category (blog) in WP.
    """
    logger.info("Query for all blogs found in b2Evolution")
    b2e_blogs_query = wpQueryHelper.getSelectB2AllBlogs()
    # https://stackoverflow.com/a/75691255/512139
    b2MySqlCursor = b2Connection.cursor(dictionary=True)
    b2MySqlCursor.execute(b2e_blogs_query)
    allBlogsResult = b2MySqlCursor.fetchall()
    
    if allBlogsResult is None:
        logger.error("No blogs found, exit")
        sys.exit("No blogs found")
    else:
        # Get all blogs from b2 and add as main categories in WP
        wpMySqlCursor = wpConnection.cursor()
        # Query to insert each main category
        wp_terms_insert = wpQueryHelper.getInsertMainCatetgories()
        wp_terms_taxonomy_insert = wpQueryHelper.getInsertWpTermTaxonomy()
        for row in allBlogsResult:
            allCategoriesQuery = wpQueryHelper.getSelectB2AllTopCategoriesForBlog()
            allCategoriesValues = (row["blog_id"],)
            logger.debug("Now get all top categories for blog: %s", allCategoriesValues)
            b2MySqlCursor.execute(allCategoriesQuery, allCategoriesValues)
            allCategoriesResult = b2MySqlCursor.fetchall()
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                for row in allCategoriesResult:
                    logger.debug("%s",row)
            if allCategoriesResult is None:
                logger.error("No top categories found for blog %s", row["blog_id"])
                sys.exit("No top categories found for blog %s", row["blog_id"])
            else:
                for row in allCategoriesResult:
                    allChildCategoriesQuery = wpQueryHelper.getSelectB2AllChildCategories()
                    allChildCategoriesValues = (row["cat_blog_ID"], row["cat_id"])
                    logger.debug("Now get all child categories for blog: %s", allChildCategoriesValues)
                    b2MySqlCursor.execute(allChildCategoriesQuery, allChildCategoriesValues)
                    allChildCategoriesResult = b2MySqlCursor.fetchall()
                    if logging.getLogger().isEnabledFor(logging.DEBUG):
                        for row in allChildCategoriesResult:
                            logger.debug("%s",row)    
    
    
    
        
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
    
    # Start by getting all blogs from b2 and adding them as top level categories on WP
    doBlogs()
    
    # Then get all categories from b2 and add them as subcategories to the main categories in WP
    doCategories()
    
    # Wrap up
    b2Connection.close()
    wpConnection.close()
if __name__ == "__main__":
    main()