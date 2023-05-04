import pandas as pd
import logging
from pathlib import Path


# Set up the logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



def score_model(test: pd.DataFrame, model, config: dict) -> pd.DataFrame:
    """
    Scores the model using the test dataset and the provided configuration.

    Args:
        test: A DataFrame containing the test dataset.
        model: The trained model object.
        config: A dictionary containing the configuration parameters for scoring.

    Returns:
        A DataFrame containing the predicted probabilities and binary predictions.
    """

    try:
        initial_features = config["initial_features"]

        ypred_proba_test = model.predict_proba(test[initial_features])[:, 1]
        ypred_bin_test = model.predict(test[initial_features])

        scores = pd.DataFrame({'predicted_probability': ypred_proba_test,
                               'predicted_binary': ypred_bin_test})
        logger.info("Model scored successfully.")
        return scores
    except Exception as e:
        logger.error(f"Error while scoring the model: {e}")
        raise


def save_scores(scores: pd.DataFrame, file_path: str):
    """
    Save the scores DataFrame to a CSV file.

    Args:
        scores: A DataFrame containing the predicted probabilities and binary predictions.
        file_path: The path where the CSV file should be saved.
    """

    try:
        scores.to_csv(file_path, index=False)
        logger.info(f"Scores saved successfully at {file_path}")
    except Exception as e:
        logger.error(f"Error while saving the scores: {e}")
        raise






# Test Code ================================================================================================================

import yaml
with open("config/default-config.yaml", 'r') as file:
    config = yaml.safe_load(file)


test_file_path = "/Users/lijiusi/Documents/2. 研究生/3. Spring Quarter/MSiA423 Cloud Engineering/Homework/hw2/CloudAssignment2_JiusiLi/test_result_folder/models/test.csv"
test = pd.read_csv(test_file_path)

import pickle
model_file_path = "/Users/lijiusi/Documents/2. 研究生/3. Spring Quarter/MSiA423 Cloud Engineering/Homework/hw2/CloudAssignment2_JiusiLi/test_result_folder/models/model.pkl"
with open(model_file_path, 'rb') as f:
    model = pickle.load(f)


score_df = score_model(test, model, config['score_model'])
save_scores(score_df, "/Users/lijiusi/Documents/2. 研究生/3. Spring Quarter/MSiA423 Cloud Engineering/Homework/hw2/CloudAssignment2_JiusiLi/test_result_folder/models/scores.csv")
