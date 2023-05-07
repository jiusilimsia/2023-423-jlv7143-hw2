import logging
import pandas as pd


# Set up the logger
logger = logging.getLogger(__name__)


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

        scores = pd.DataFrame({"predicted_probability": ypred_proba_test,
                               "predicted_binary": ypred_bin_test})
        logger.info("Model scored successfully.")
        return scores
    except KeyError as e:
        logger.error("Error while scoring the model due to missing key in config: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while scoring the model: %s", e)
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
        logger.info("Scores saved successfully at %s", file_path)
    except FileNotFoundError as e:
        logger.error("Error while saving the scores: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error while saving the scores: %s", e)
        raise
