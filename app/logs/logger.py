import logging
from pathlib import Path
import sys

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt="{asctime} | {levelname} | {message}", style="{", datefmt="%Y-%m-%d %H:%M:%S"
)

path_to_log = Path(__file__).resolve().parent / "app.log"
file_handler = logging.FileHandler(filename=path_to_log, mode="a", encoding="utf-8")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.WARNING)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
