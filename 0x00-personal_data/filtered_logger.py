#!/usr/bin/env python3
""" Module contains a function that returns a log message obfuscated
"""
import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str,
                 seperator: str) -> str:
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
    pattern = r"({})=([^{}]*)".format('|'.join(fields), seperator)
    return re.sub(pattern, r"\1={}".format(redaction), message)
