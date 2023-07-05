from typing import List
import logging
from functools import wraps
from contextlib import contextmanager
from copy import deepcopy

from src.logger.config import SETTINGS


DEFAULT_TAGS = ["GENERAL"]
DEFAULT_LEVEL = logging.DEBUG
LOGGER_NAME = "hosting-airbnb-prices"


def str_to_level(level: str):
    """Convert a string to a logging level"""
    return getattr(logging, level.upper())


class AppLogger:
    def __init__(self, log_file: str = None, debug_logs: bool = False):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.logger.setLevel(DEFAULT_LEVEL)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            print(f"Logging to {log_file}")

        if debug_logs:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)
            print("Logging to console")

        self.level = DEFAULT_LEVEL
        self.using_default_tags: List[str] = deepcopy(DEFAULT_TAGS)
        self.allow_tags: List[str] = deepcopy(DEFAULT_TAGS)

    def add_allowed_tags(self, tags: List[str]) -> None:
        self.allow_tags.extend(tags)

    def set_level(self, level: str) -> None:
        if isinstance(level, str):
            level = getattr(logging, level.upper())
        self.logger.setLevel(level)
        self.level = level

    def can_log(self, tags: List[str]) -> bool:
        """Check if the logger can log with any of the tags provided"""
        if not isinstance(tags, list):
            tags = [tags]
        if any(not isinstance(tag, str) for tag in tags):
            raise TypeError(f"Tags must be strings, got {tags}")

        return any(tag in self.allow_tags for tag in tags)

    def log(
        self,
        message: str,
        tags: List[str] = None,
        level: str = None,
    ) -> None:
        """
        Log a message with an optional tag
        Args:
            message (str): The message to log
            tags (List[str]): The tags to log the message with, if no tag is provided,
                the default tags will be used
            level (str): The level to log the message with
        """
        tags = tags or self.using_default_tags
        level = level or self.level

        if self.can_log(tags):
            self.logger.log(level, message, extra={"tag": tags})

    def wrap_func(self, tags: List[str] = None, level: str = None):
        """
        Decorator to add tags and set level to a function
        Args:
            tags (List[str]): The tags to add to the function
            level (str): The level to set to the function
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                original_tags = deepcopy(self.using_default_tags)
                original_level = self.level

                if tags is not None:
                    self.using_default_tags.extend(tags)
                if level is not None:
                    self.set_level(level)

                result = func(*args, **kwargs)

                self.using_default_tags = original_tags
                self.set_level(original_level)

                return result

            return wrapper

        return decorator

    @contextmanager
    def wrap_block(self, tags: List[str] = None, level: str = None):
        """
        Context manager to add tags and set level for a block of code
        Args:
            tags (List[str]): The tags to add to the block of code
            level (str): The level to set for the block of code
        """
        original_tags = deepcopy(self.using_default_tags)
        original_level = self.level

        if tags is not None:
            self.using_default_tags.extend(tags)
        if level is not None:
            self.set_level(level)

        try:
            yield
        finally:
            self.using_default_tags = original_tags
            self.set_level(original_level)


logger = AppLogger(
    log_file=SETTINGS["LOG_FILE"],
    debug_logs=SETTINGS["DEBUG_LOGS"],
)
logger.allow_tags = SETTINGS["ALLOWED_TAGS"]
logger.set_level(SETTINGS["LOG_LEVEL"])
