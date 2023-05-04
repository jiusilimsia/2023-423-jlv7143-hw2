import logging
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

# Set up the logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
            ax.hist([
                data[target == 0][feat].values, data[target == 1][feat].values
            ])
            ax.set_xlabel(' '.join(feat.split('_')).capitalize())
            ax.set_ylabel('Number of observations')

            # Save the figure to the specified directory with a descriptive file name
            fig_path = dir / f"{feat}_histogram.png"
            fig.savefig(fig_path)
            # Add the saved figure's path to the list of saved figure paths
            saved_fig_paths.append(fig_path)

        logger.info("Histogram figures saved successfully.")
    except Exception as e:
        logger.error(f"Error while saving histogram figures: {e}")
        raise

    return saved_fig_paths






# Test Code ================================================================================================================

import yaml
# Load the YAML configuration
with open("config/default-config.yaml", 'r') as yaml_file:
    config = yaml.safe_load(yaml_file)

file_path = "/Users/lijiusi/Documents/2. 研究生/3. Spring Quarter/MSiA423 Cloud Engineering/Homework/hw2/CloudAssignment2_JiusiLi/test_result_folder/generated_data.csv"
# Read the data from the CSV file into a pandas DataFrame
data = pd.read_csv(file_path)

save_figures(data, Path("test_result_folder/figures/"), config['analysis'])