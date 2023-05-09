import logging
import sys
from pathlib import Path
from time import sleep
import requests
from requests.exceptions import RequestException


logger = logging.getLogger(__name__)


def get_data(
    url: str, attempts: int = 4, wait: int = 3, wait_multiple: int = 2
) -> bytes:
    """Acquires data from URL

    Args:
        url: The URL to download data from.
        attempts: The number of download attempts.
        wait: The initial waiting time between download attempts.
        wait_multiple: The multiple of the waiting time to increase after each failed attempt.

    Returns:
        The content of the downloaded data as bytes.

    Raises:
        RuntimeError: If the data could not be downloaded after the specified number of attempts.
    """
    for attempt in range(attempts):
        try:
            response = requests.get(url)
            response.raise_for_status()
            logger.debug("Acquire data from web successfully")

        except RequestException as e:
            if attempt < attempts - 1:
                logger.warning(
                    "Error downloading data (attempt %d/%d): %s",
                    attempt + 1,
                    attempts,
                    e,
                )
                sleep(wait)
                wait *= wait_multiple
            else:
                logger.error(
                    "Failed to download data from %s after %s attempts", url, attempts
                )
                raise RuntimeError(
                    "Failed to download data from %s after %s attempts"
                    % (url, attempts)
                ) from e

        return response.content


def write_data(url_contents: bytes, save_path: Path) -> None:
    """Writes data from url to a file

    Args:
        url_contents: The data download from url to be written to the file, as bytes.
        save_path: The path where the file should be saved.

    Raises:
        FileNotFoundError: If the specified path does not exist.
    """
    try:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "wb") as file:
            file.write(url_contents)
        logger.info("Data written to %s successfully", save_path)
    except FileNotFoundError as e:
        logger.error("Error writing data to %s: %s", save_path, e)
        raise
    except Exception as e:
        logger.error("Error writing data to %s: %s", save_path, e)
        raise


def acquire_data(url: str, save_path: Path) -> None:
    """Acquires data from specified URL

    Args:
        url: URL for where data to be acquired is stored
        save_path: Local path to write data to
    """
    url_contents = get_data(url)
    try:
        write_data(url_contents, save_path)
    except FileNotFoundError:
        logger.critical("Please provide a valid file location to save dataset to.")
        sys.exit(1)
    except Exception as e:
        logger.error("Error occurred while trying to write dataset to file: %s", e)
