

class datbaseManager:
    """Database Helper class"""
    def __init__(self):
      self.conn = None
      
    """
    $b2e_db_host = 'localhost';
    $b2e_db_user = 'b2evolution_user';
    $b2e_db_pass = 'b2evolution_password';
    $b2e_db_name = 'b2evolution_db';
    """
    def openConnection(db_host,db_user,db_pass,db_name):
        pass