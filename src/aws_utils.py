from pathlib import Path

import boto3

import logging
logger = logging.getLogger(__name__)


def upload_artifacts(artifacts: Path, config: dict) -> list[str]:
    """Upload all the artifacts in the specified directory to S3


    Args:
        artifacts: Directory containing all the artifacts from a given experiment
        config: Config required to upload artifacts to S3; see example config file for structure

    Returns:
        List of S3 uri's for each file that was uploaded
    """
    raise NotImplementedError








def upload_artifacts(artifacts: Path, config: dict) -> list[str]:
    """Upload all the artifacts in the specified directory to S3

    Args:
        artifacts: Directory containing all the artifacts from a given experiment
        config: Config required to upload artifacts to S3; see example config file for structure

    Returns:
        List of S3 uri's for each file that was uploaded
    """
    s3 = boto3.client("s3", **config)

    try:
        s3_uri_prefix = config["s3_uri_prefix"].strip("/")
        bucket_name = config["bucket_name"]
        bucket_prefix = config.get("bucket_prefix", "").strip("/")

        # Get a list of all files in the artifacts directory
        artifact_files = list(artifacts.glob("**/*"))

        # Upload each file to S3
        s3_uris = []
        for file_path in artifact_files:
            # Skip directories
            if file_path.is_dir():
                continue

            # Get the S3 key by stripping the artifacts directory and joining with the S3 prefix and bucket prefix
            s3_key = str(file_path.relative_to(artifacts)).replace("\\", "/")
            s3_uri = f"s3://{bucket_name}/{bucket_prefix}/{s3_key}".strip("/")
            s3.upload_file(str(file_path), bucket_name, f"{bucket_prefix}/{s3_key}")

            s3_uris.append(s3_uri)
            logger.debug(f"{file_path} uploaded to S3 as {s3_uri}")

        logger.info(f"Uploaded {len(s3_uris)} files to S3 under s3://{bucket_name}/{bucket_prefix}")
        return s3_uris
    except Exception as e:
        logger.error(f"Error uploading artifacts to S3: {e}")
        raise
