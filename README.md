# Clouds
Northwestern MSiA Jiusi Li

## Overview of the pipeline

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


## Project set up instructions
The setup process of the project (installing requirements, fetching data, etc.) are included in the Dockerfile and pipeline:

No need to do it manually. **Only need to build Docker image and build&run Docker container.**


## Docker image and container

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





