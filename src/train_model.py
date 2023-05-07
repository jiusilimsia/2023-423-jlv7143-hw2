import pandas as pd
import pickle
import sklearn.model_selection
import sklearn.ensemble
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def train_model(data: pd.DataFrame, config: dict):
    """
    Trains a model using the specified data and configuration.

    Args:
        data: A DataFrame containing the features and target variable.
        config: A dictionary containing the configuration parameters for the model.

    Returns:
        model: A trained model object.
        train_df: A DataFrame containing the training data (X_train and y_train).
        test_df: A DataFrame containing the test data (X_test and y_test).
    """
    try:

        target = config.get("target")
        test_size = config.get("test_size")
        initial_features = config.get("initial_features")
        model_params = config.get("model_params")

        X = data.drop(columns=[target])
        y = data[target]

        # Split data into train/test set and train model based on config
        X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
            X, y, test_size=test_size)
        logger.debug("Train test split finished")

        model = sklearn.ensemble.RandomForestClassifier(**model_params)
        model.fit(X_train[initial_features], y_train)
        logger.debug("Model training finished")

        # Combine X_train and y_train into a single DataFrame
        train_df = X_train.copy()
        train_df[target] = y_train

        # Combine X_test and y_test into a single DataFrame
        test_df = X_test.copy()
        test_df[target] = y_test

        logger.info("Model training finished, train and test data generated")
        return model, train_df, test_df
    
    except KeyError as e:
        logger.error("Missing key in the configuration: %s", e)
        raise
    except ValueError as e:
        logger.error("Invalid value encountered: %s", e)
        raise
    except Exception as e:
        logger.error("Error while training the model: %s", e)
        raise


def save_data(train: pd.DataFrame, test: pd.DataFrame, artifacts: Path):
    """
    Saves the training and test data to disk as CSV files.

    Args:
        train: A DataFrame containing the training data.
        test: A DataFrame containing the test data.
        artifacts: A Path object representing the directory where the data should be saved.
    """
    try:
        train.to_csv(artifacts / "train.csv", index=False)
        test.to_csv(artifacts / "test.csv", index=False)
        logger.info("Train and test data saved successfully.")
    except FileNotFoundError as e:
        logger.error("Error while saving train and test data: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while saving train and test data: %s", e)
        raise


def save_model(model, file_path: Path):
    """
    Saves the trained model object to disk as a pickle file.

    Args:
        model: A trained model object.
        file_path: A Path object representing the path to the file where the model should be saved.
    """
    try:
        with open(file_path, "wb") as f:
            pickle.dump(model, f)
        logger.info("Model saved successfully at %s", file_path)
    except FileNotFoundError as e:
        logger.error("Error while saving the model: %s", e)
        raise
    except pickle.PicklingError as e:
        logger.error("Error while pickling the model: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while saving the model: %s", e)
        raise







# Test Code ================================================================================================================

# file_path = "/Users/lijiusi/Documents/2. 研究生/3. Spring Quarter/MSiA423 Cloud Engineering/Homework/hw2/CloudAssignment2_JiusiLi/test_result_folder/generated_data.csv"
# # Read the data from the CSV file into a pandas DataFrame
# data = pd.read_csv(file_path)

# import yaml
# # Read the YAML configuration file
# with open("config/default-config.yaml", 'r') as file:
#     config = yaml.safe_load(file)



# model_config = config['train_model']
# model, train_df, test_df = train_model(data, model_config)


# save_data(train_df, test_df, Path("/Users/lijiusi/Documents/2. 研究生/3. Spring Quarter/MSiA423 Cloud Engineering/Homework/hw2/CloudAssignment2_JiusiLi/test_result_folder/models"))
# save_model(model, Path("/Users/lijiusi/Documents/2. 研究生/3. Spring Quarter/MSiA423 Cloud Engineering/Homework/hw2/CloudAssignment2_JiusiLi/test_result_folder/models/model.pkl"))
