import re
import logging

from datetime import datetime

class ConversionHelper:
    
    
    @staticmethod
    def sanitize_title(title):
        """
        Sanitize the given title to create a slug.

        :param title: The title to sanitize.
        :return: A sanitized slug.
        """
        return re.sub(r'[^a-z0-9]+', '-', title.strip().lower())

    @staticmethod
    def convert_date(date):
        """
        Convert the given date to the format 'Y-m-d H:i:s'.

        :param date: The date to convert.
        :return: The converted date as a string.
        """
        logger = logging.getLogger(__name__)  # Obtain the logger for this module
        if isinstance(date, datetime):
            logger.debug("Date is already a datetime object")
            return date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')