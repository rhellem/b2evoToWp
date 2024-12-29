class wpQueryHelper:
    @staticmethod
    def getInsertMainCatetgories():
          return """
            INSERT INTO wp_terms (term_id, name, slug)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE name = VALUES(name), slug = VALUES(slug)
        """
        
    @staticmethod
    def getInsertWpTermTaxonomy():
        # Category is fixed
        return """
            INSERT INTO wp_term_taxonomy (term_id, taxonomy, description,parent) VALUES 
            (%s, %s, %s,%s)
        """