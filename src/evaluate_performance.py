import logging
from pathlib import Path
import pandas as pd
import sklearn.metrics
import yaml

# Set up the logger
logger = logging.getLogger(__name__)


def evaluate_performance(scores: pd.DataFrame, test: pd.DataFrame, config: dict) -> dict:
    """
    Evaluates the performance of a model based on the provided scores and configuration.

    Args:
        scores: A DataFrame containing the predicted probabilities and binary predictions.
        test: A pandas DataFrame containing the test data.
        config: A dictionary containing the configuration parameters for evaluation.

    Returns:
        A dictionary containing the evaluation metrics.
    """

    try:
        y_true = test[config["target"]]
        ypred_proba = scores[config["prob_col"]]
        ypred_bin = scores[config["bin_col"]]

        auc = sklearn.metrics.roc_auc_score(y_true, ypred_proba)
        logger.debug("AUC calculated.")
        confusion = sklearn.metrics.confusion_matrix(y_true, ypred_bin)
        logger.debug("Confusion matrix calculated.")
        accuracy = sklearn.metrics.accuracy_score(y_true, ypred_bin)
        logger.debug("Accuracy calculated.")
        classification_report = sklearn.metrics.classification_report(y_true, ypred_bin)
        logger.debug("Classification report calculated.")

        metrics = {
            "AUC": auc,
            "Confusion Matrix": confusion.tolist(),
            "Accuracy": accuracy,
            "Classification Report": classification_report
        }
        logger.info("Performance evaluation completed successfully.")
        return metrics
    except Exception as e:
        logger.error("Error while evaluating performance: %s", e)
        raise


def save_metrics(metrics: dict, file_path: Path):
    """
    Save the evaluation metrics to a YAML file.

    Args:
        metrics: A dictionary containing the evaluation metrics.
        file_path: The path where the YAML file should be saved.
    """

    try:
        # Convert numpy scalar values to Python built-in types
        metrics["AUC"] = float(metrics["AUC"])
        metrics["Accuracy"] = float(metrics["Accuracy"])
        metrics["Confusion Matrix"] = metrics["Confusion Matrix"]

        with open(file_path, "w") as f:
            yaml.dump(metrics, f, default_flow_style=False)
        logger.info("Metrics saved successfully at %s", file_path)
    except FileNotFoundError as e:
        logger.error("Error while saving the metrics: %s", e)
        raise
    except Exception as e:
        logger.error("Error while saving metrics: %s", e)
        raise
