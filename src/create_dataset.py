import yaml
import pandas as pd
import numpy as np

def create_dataset(raw_data_path, config):
    """
    Create a dataset from the raw data.

    Args:
        raw_data_path: The path to the raw data file.
        config: A dictionary containing the dataset configuration, such as columns.

    Returns:
        A pandas DataFrame containing the processed dataset.
    """

    columns = config["columns"]
    cloud_data_index = config["cloud_data_index"]

    with open(raw_data_path, 'r') as f:
        data = [[s for s in line.split(' ') if s != ''] for line in f.readlines()]

    first_cloud = data[cloud_data_index["cloud1"][0]:cloud_data_index["cloud1"][1]]
    first_cloud = [[float(s.replace('/n', '')) for s in cloud] for cloud in first_cloud]
    first_cloud = pd.DataFrame(first_cloud, columns=columns)
    first_cloud['class'] = np.zeros(len(first_cloud))

    second_cloud = data[cloud_data_index["cloud2"][0]:cloud_data_index["cloud2"][1]]
    second_cloud = [[float(s.replace('/n', '')) for s in cloud] for cloud in second_cloud]
    second_cloud = pd.DataFrame(second_cloud, columns=columns)
    second_cloud['class'] = np.ones(len(second_cloud))

    combined_data = pd.concat([first_cloud, second_cloud])
    return combined_data

def save_dataset(data, save_data_path):
    """
    Save the dataset to a CSV file.

    Args:
        data: A pandas DataFrame containing the dataset.
        save_data_path: The path where the CSV file should be saved.
    """

    data.to_csv(save_data_path, index=False)





# Test Code ================================================================================================================

import yaml

# Read the YAML configuration file
with open("config/default-config.yaml", 'r') as file:
    config = yaml.safe_load(file)

# Create the dataset using the configuration values
dataset = create_dataset(config["create_dataset"]["path"]["raw_data_path"], config["create_dataset"])

# Save the dataset using the configuration values
save_dataset(dataset, config["create_dataset"]["path"]["save_data_path"])