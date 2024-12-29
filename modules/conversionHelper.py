import re

class ConversionHelper:
    @staticmethod
    def sanitize_title(title):
        """
        Sanitize the given title to create a slug.

        :param title: The title to sanitize.
        :return: A sanitized slug.
        """
        return re.sub(r'[^a-z0-9]+', '-', title.strip().lower())