class wpQueryHelper:
    @staticmethod
    def getInsertWpCatetgory():
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
        
    @staticmethod
    def getSelectB2AllBlogs():
        return """
            SELECT blog_id, blog_name, blog_shortname
            FROM evo_blogs
        """
        
    @staticmethod
    def getSelectB2AllTopCategoriesForBlog():
        return """
            SELECT cat_id, cat_name, cat_blog_ID,cat_urlname
            FROM evo_categories
            WHERE cat_blog_ID = %s AND cat_parent_ID IS NULL
        """
        
    @staticmethod
    def getSelectB2AllChildCategories():
        return """
            SELECT cat_id, cat_name, cat_blog_ID, cat_parent_ID,cat_urlname
            FROM evo_categories
            WHERE cat_blog_ID = %s AND cat_parent_ID = %s
        """