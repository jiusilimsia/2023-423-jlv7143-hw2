import logging
import pandas as pd
import numpy as np


# Set up the logger
logger = logging.getLogger(__name__)


def create_dataset(raw_data_path: str, config: dict) -> pd.DataFrame:
    """
    Create a dataset from the raw data.

    Args:
        raw_data_path: The path to the raw data file.
        config: A dictionary containing the dataset configuration, such as columns.

    Returns:
        A pandas DataFrame containing the processed dataset.
    """

    try:
        columns = config["columns"]
        cloud_data_index = config["cloud_data_index"]

        with open(raw_data_path, "r") as f:
            data = [[s for s in line.split(" ") if s != ""] for line in f.readlines()]
        logger.debug("Data read successfully.")

        first_cloud = data[cloud_data_index["cloud1"][0] : cloud_data_index["cloud1"][1]]
        first_cloud = [[float(s.replace("/n", "")) for s in cloud] for cloud in first_cloud]
        first_cloud = pd.DataFrame(first_cloud, columns=columns)
        first_cloud["class"] = np.zeros(len(first_cloud))

        second_cloud = data[cloud_data_index["cloud2"][0] : cloud_data_index["cloud2"][1]]
        second_cloud = [[float(s.replace("/n", "")) for s in cloud] for cloud in second_cloud]
        second_cloud = pd.DataFrame(second_cloud, columns=columns)
        second_cloud["class"] = np.ones(len(second_cloud))

        combined_data = pd.concat([first_cloud, second_cloud])
        logger.info("Dataset created successfully.")

    except FileNotFoundError as e:
        logger.error("Error opening the raw data file: File not found %s", e)
        raise
    except IOError as e:
        logger.error("Error reading the raw data file: %s", e)
        raise
    except KeyError as e:
        logger.error("Error in the configuration: Missing key %s", e)
        raise
    except Exception as e:
        logger.error("Error while creating the dataset: %s", e)
        raise

    return combined_data


def save_dataset(data: pd.DataFrame, save_data_path: str):
    """
    Save the dataset to a CSV file.

    Args:
        data: A pandas DataFrame containing the dataset.
        save_data_path: The path where the CSV file should be saved.
    """

    try:
        data.to_csv(save_data_path, index=False)
        logger.info("Dataset saved successfully at %s", save_data_path)
    except FileNotFoundError as e:
        logger.error(
            "Error while saving the dataset: File path not found: %s: %s", save_data_path, e
        )
        raise
    except PermissionError as e:
        logger.error(
            "Error while saving the dataset: Permission denied for file path: %s: %s",
            save_data_path, e
        )
        raise
    except Exception as e:
        logger.error("Error while saving the dataset: %s", e)
        raise
