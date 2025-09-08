import logging
from pathlib import Path
import sys

# Creation of a logger object
logger = logging.getLogger("file-organize-tool")
logger.setLevel(logging.DEBUG)

# Creating a format for log formatting
formatter = logging.Formatter(
    fmt="{asctime} | {levelname} | {message}", style="{", datefmt="%Y-%m-%d %H:%M:%S"
)

# Creating a file handler for logging
path_to_log = Path(__file__).resolve().parent / "app.log"
file_handler = logging.FileHandler(filename=path_to_log, mode="a", encoding="utf-8")
file_handler.setFormatter(formatter)

# Creating a console handler for logging
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.WARNING)

""" 
Adds handlers to the logger so that log messages are sent both to the file and to the console, according to the configured level and format.
"""
logger.addHandler(file_handler)
logger.addHandler(console_handler)
