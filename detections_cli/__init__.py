import logging

from decouple import config

logging.basicConfig(
    level=config("LOGGING_LEVEL"),
    format="%(asctime)s | %(levelname)s | %(funcName)s | %(message)s",
    datefmt="%d-%b-%y %H:%M:%S %Z",
    handlers=[logging.StreamHandler()],
    encoding="utf-8",
)

LOGGER = logging.getLogger()
