# Clouds
Northwestern University MSiA Jiusi Li

## Overview of the Pipeline

The pipeline is designed to classify clouds through a machine learning model. The pipeline involves the following steps:

1. Acquire raw data from an online source.
2. Preprocess and structure the data into a usable format.
3. Enrich the dataset with relevant features.
4. Perform exploratory data analysis, generating statistics and visualizations.
5. Split the data into training and testing sets and train the model.
6. Score the model on the test set.
7. Evaluate the model's performance metrics.
8. Save all artifacts, including data, models, and metrics.
9. Optionally, upload the artifacts to an AWS S3 bucket.

The intent of this pipeline is to automate the process of obtaining, preprocessing, training, and evaluating a cloud classification model, while maintaining traceability and organization of the generated artifacts.

## Project Structure

<pre>

project
│
├── config
│   ├── default-config.yaml:   Configuration for logging settings
│   └── logging
│       └── local.conf:   Configuration for the whole pipeline
│
├── dockerfiles
│   ├── Dockerfile:   Building the Docker image used to run the main model pipeline
│   └── Dockerfile_unittest (for unit test only):   Building the Docker image used to run unit tests
│
├── src
│   ├── acquire_data.py
│   ├── analysis.py
│   ├── aws_utils.py
│   ├── create_dataset.py
│   ├── evaluate_performance.py
│   ├── generate_features.py
│   ├── score_model.py
│   └── train_model.py
│
├── pipeline.py:   The main script that orchestrates the execution of the entire model pipeline
├── requirements.txt:   Listing required packages and dependencies for the whole pipeline
├── tests (for unit test only)
│   └── generate_features_test.py:   Unit test for generate_features.py code
└── requirements_unittest.txt (for unit test only):   Listing required packages and dependencies for running unit tests.

</pre>


## Project Setup Instructions

To retrieve the code of the project, you need to clone the repository using the following command:

```bash
git clone https://github.com/MSIA/2023-423-jlv7143-hw2.git
```

### To run the pipeline in your local machine:

- First login to refresh credentials

    ```shell
    aws sso login --profile <your_aws_profile_name>
    ```

- Then set up our python environment

    ```shell
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

- Finally authenticate your boto3 calls and run the pipeline with the command below:

    ```shell
    export AWS_PROFILE=<your_aws_profile_name>
    python app.py
    ```

For the setup process for running the project (installing requirements, fetching data, etc.) in a Docker container, refer to the **Docker image and container** section.



## Docker Image and Container

Before we start, please make sure you already configured the AWS CLI with AWS SSO.

### Build the Docker image

```bash
docker build -f dockerfiles/Dockerfile -t <image_name> .
```

### Run the entire model pipeline

Set the AWS_PROFILE environment variable to the AWS profile you want to use; 
Build the Docker container; 
Run the model pipeline; 
```bash
docker run -v ~/.aws:/root/.aws -e AWS_PROFILE=<your_aws_profile_name> <image_name>
```

### Build the Docker image for tests

```bash
docker build -f dockerfiles/Dockerfile_unittest -t <image_name> .
```

### Run the tests

```bash
docker run -it  <image_name>
```





