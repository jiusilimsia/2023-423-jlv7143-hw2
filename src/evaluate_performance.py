import pandas as pd
import sklearn.metrics
import logging
from pathlib import Path
import yaml

# Set up the logger
logger = logging.getLogger(__name__)


def evaluate_performance(scores: pd.DataFrame, y_true: pd.Series, config: dict) -> dict:
    """
    Evaluates the performance of a model based on the provided scores and configuration.

    Args:
        scores: A DataFrame containing the predicted probabilities and binary predictions.
        y_true: A pandas Series containing the true labels for the test data.
        config: A dictionary containing the configuration parameters for evaluation.

    Returns:
        A dictionary containing the evaluation metrics.
    """

    try:
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
        logger.error(f"Error while evaluating performance: {e}")
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

        with open(file_path, 'w') as f:
            yaml.dump(metrics, f, default_flow_style=False)
        logger.info(f"Metrics saved successfully at {file_path}")
    except FileNotFoundError as e:
        logger.error("Error while saving the metrics: %s", e)
        raise
    except Exception as e:
        logger.error(f"Error while saving metrics: {e}")
        raise






# Test Code ================================================================================================================

# import yaml
# # Load the YAML configuration
# with open("config/default-config.yaml", 'r') as yaml_file:
#     config = yaml.safe_load(yaml_file)

# # Example data
# score_file_path = "/Users/lijiusi/Documents/2. 研究生/3. Spring Quarter/MSiA423 Cloud Engineering/Homework/hw2/CloudAssignment2_JiusiLi/test_result_folder/models/scores.csv"
# # Read the data from the CSV file into a pandas DataFrame
# scores = pd.read_csv(score_file_path)

# test_file_path = "/Users/lijiusi/Documents/2. 研究生/3. Spring Quarter/MSiA423 Cloud Engineering/Homework/hw2/CloudAssignment2_JiusiLi/test_result_folder/models/test.csv"
# test = pd.read_csv(test_file_path)

# metrics = evaluate_performance(scores, test[config['evaluate_performance']['target']], config['evaluate_performance'])
# save_metrics(metrics, Path("/Users/lijiusi/Documents/2. 研究生/3. Spring Quarter/MSiA423 Cloud Engineering/Homework/hw2/CloudAssignment2_JiusiLi/test_result_folder/models/metrics.yaml"))