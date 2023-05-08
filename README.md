# Clouds

## Build the Docker image

```bash
cd <path_to_root_directory_of_the_project>
docker build -f dockerfiles/Dockerfile -t <image_name> .
```

## Run the entire model pipeline

Set the AWS_PROFILE environment variable to the AWS profile you want to use; 
Build the Docker container; 
Run the model pipeline; 
```bash
docker run -v ~/.aws:/root/.aws -e AWS_PROFILE=<your_aws_profile_name> <image_name>
```


## Build the Docker image for tests

```bash
cd <path_to_root_directory_of_the_project>
docker build -f dockerfiles/Dockerfile_unittest -t <image_name> .
```

### Run the tests

```bash
docker run -it  <image_name>
```





