from pathlib import Path

import boto3

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def upload_artifacts(artifacts: Path, config: dict) -> list[str]:
    """Upload all the artifacts in the specified directory to S3


    Args:
        artifacts: Directory containing all the artifacts from a given experiment
        config: Config required to upload artifacts to S3; see example config file for structure

    Returns:
        List of S3 uri's for each file that was uploaded
    """
    raise NotImplementedError
