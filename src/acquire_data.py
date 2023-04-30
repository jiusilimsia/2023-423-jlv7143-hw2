import logging
import sys
import time
from pathlib import Path

import requests

logger = logging.getLogger(__name__)


def get_data(url: str, attempts: int = 4, wait: int = 3, wait_multiple: int = 2) -> bytes:
    """Acquires data from URL

    ...

    """
    raise NotImplementedError


def acquire_data(url: str, save_path: Path) -> None:
    """Acquires data from specified URL

    Args:
        url: URL for where data to be acquired is stored
        save_path: Local path to write data to
    """
    url_contents = get_data(url)
    try:
        write_data(url_contents, save_path)
        logger.info("Data written to %s", save_path)
    except FileNotFoundError:
        logger.error("Please provide a valid file location to save dataset to.")
        sys.exit(1)
    except Exception as e:
        logger.error("Error occurred while trying to write dataset to file: %s", e)
        sys.exit(1)
