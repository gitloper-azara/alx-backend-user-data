#!/usr/bin/env python3
""" PII Obfuscation """
import logging
from typing import List
import re


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """ Returns a log message while obfuscating PII

    Args:
        fields: All fields in the message to obfuscate
        redaction: string representing obfuscated fields
        message: the log line
        separator: character that separates all fields in the log line
    """
    for field in fields:
        regex = fr'(?<={field}=)[^{separator}]*'
        message = re.sub(regex, redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records using filter_datum()

        Args:
            record: information or event being logged.
        """
        return filter_datum(
            self.fields, self.REDACTION, super().format(record),
            self.SEPARATOR
        )


def get_logger() -> logging.Logger:
    """ A function that returns a logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter())
    logger.addHandler(stream_handler)
    return logger
