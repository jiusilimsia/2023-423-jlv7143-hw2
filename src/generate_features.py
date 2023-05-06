import pandas as pd
import numpy as np
import logging

# Set up the logger
logger = logging.getLogger(__name__)


def generate_features(data: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Generates features for a dataset using a configuration dictionary.
    
    Args:
        data (pd.DataFrame): The input dataset.
        config (dict): A dictionary containing the feature generation configuration.
        
    Returns:
        pd.DataFrame: The processed dataset with the new features and the target variable.
    """

    try:
        # Perform log transformation for specified columns in the configuration
        log_transform = config["log_transform"]
        for new_feature, col in log_transform.items():
            data[new_feature] = data[col].apply(np.log)

        # Perform multiplication for specified column pairs in the configuration
        multiply = config["multiply"]
        for new_feature, cols in multiply.items():
            data[new_feature] = data[cols["col_a"]].multiply(data[cols["col_b"]])

        # Calculate the range for specified columns in the configuration
        calculate_range = config["calculate_range"]
        for feature, cols in calculate_range.items():
            data[feature] = data[cols["max_col"]] - data[cols["min_col"]]

        # Calculate the normalized range for specified columns in the configuration
        calculate_norm_range = config["calculate_norm_range"]
        for new_feature, cols in calculate_norm_range.items():
            data[new_feature] = (data[cols["max_col"]] - data[cols["min_col"]]).divide(data[cols["mean_col"]])

        logger.info("Features generated successfully.")
    except Exception as e:
        logger.error(f"Error while generating features: {e}")
        raise

    return data


def save_dataset(data: pd.DataFrame, save_data_path: str):
    """
    Save the dataset to a CSV file.

    Args:
        data: A pandas DataFrame containing the dataset.
        save_data_path: The path where the CSV file should be saved.
    """

    try:
        data.to_csv(save_data_path, index=False)
        logger.info(f"Dataset saved successfully at {save_data_path}")
    except Exception as e:
        logger.error(f"Error while saving the dataset: {e}")
        raise





# Test Code ================================================================================================================

# import yaml
# import create_dataset as cd

# # Load the YAML configuration
# with open("config/default-config.yaml", 'r') as yaml_file:
#     config = yaml.safe_load(yaml_file)

# # Example data
# file_path = "/Users/lijiusi/Documents/2. 研究生/3. Spring Quarter/MSiA423 Cloud Engineering/Homework/hw2/CloudAssignment2_JiusiLi/test_result_folder/processed_data.csv"
# # Read the data from the CSV file into a pandas DataFrame
# data = pd.read_csv(file_path)

# # Extract the 'generate_features' configuration
# generate_features_config = config["generate_features"]

# # Call the function with the data and the configuration
# generated_data = generate_features(data, generate_features_config)
# save_dataset(generated_data, "test_result_folder/generated_data.csv")








"""for all transformations below, the format is: 
    generate_features:
        Transformation_name: 
            generated_feature_name: target_feature
        OR 
        Transformation_name:
            Transformation on some specific features:
                target_feature_code: target_feature
"""
# generate_features:
#   calculate_norm_range:
#     IR_norm_range:
#       min_col: IR_min
#       max_col: IR_max
#       mean_col: IR_mean
#   log_transform:
#     log_entropy: visible_entropy
#   multiply:
#     entropy_x_contrast:
#       col_a: visible_contrast
#       col_b: visible_entropy