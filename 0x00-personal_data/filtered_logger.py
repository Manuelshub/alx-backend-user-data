#!/usr/bin/env python3
""" Module contains a function that returns a log message obfuscated
"""
import logging
import re
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Returns a log message obfuscated

    Arguments:
        fields (List): a list of strings representing all fields to obfuscate
        redaction (List): a list of strings representing the redaction values
        message (str): the log entry to obfuscate
        seperator (str): a character to be used as a separator between fields

    Returns:
        str: the obfuscated log entry
    """
    for f in fields:
        message = re.sub(r"{}=([^{}]*)".format(f, separator),
                         r"{}={}".format(f, redaction), message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPERATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record using the RedactingFormatter format string

        Arguments:
            record (logging.LogRecord): the log record to format

        Returns:
            str: the formatted log record
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPERATOR)


def get_logger() -> logging.Logger:
    """
    Returns a logger object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.streamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger
