import logging
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

# from cycler import cycler


# Set up the logger
logger = logging.getLogger(__name__)


def save_figures(data: pd.DataFrame, dir: Path, config: dict) -> list[Path]:
    """Saves histograms of features in the given data to the specified directory.

    Args:
        data: A DataFrame containing the features for which histograms should be created.
        dir: The directory where the histogram figures should be saved.
        config (dict): A dictionary containing the feature generation configuration.

    Returns:
        A list of Paths where the saved figures are located.
    """

    mpl.rcParams.update(config)
    saved_fig_paths = []

    try:
        # Get the feature columns and target variable column from the data
        features = data.drop("class", axis=1).columns
        target = data["class"]

        # Iterate over each feature in the DataFrame
        for feat in features:
            fig, ax = plt.subplots(figsize=(12, 8))
            # Plot a histogram for the current feature, separated by target class
            ax.hist([data[target == 0][feat].values, data[target == 1][feat].values])
            ax.set_xlabel(" ".join(feat.split("_")).capitalize())
            ax.set_ylabel("Number of observations")

            # Save the figure to the specified directory with a descriptive file name
            fig_path = dir / f"{feat}_histogram.png"
            fig.savefig(fig_path)
            # Add the saved figure's path to the list of saved figure paths
            saved_fig_paths.append(fig_path)

            logger.debug("%s histogram generated successfully.", feat)

        logger.info("Histogram figures saved successfully.")

    except FileNotFoundError as e:
        logger.error(
            "Error while saving histogram figures: Directory not found: %s: %s", dir, e
        )
        raise
    except PermissionError as e:
        logger.error(
            "Error while saving histogram figures: Permission denied for directory: %s: %s",
            dir, e
        )
        raise
    except ValueError as e:
        logger.error(
            "Error while saving histogram figures: Invalid configuration: %s", e
        )
        raise
    except Exception as e:
        logger.error("Error while saving histogram figures: %s", e)
        raise

    return saved_fig_paths
