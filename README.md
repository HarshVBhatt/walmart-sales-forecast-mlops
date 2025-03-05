# walmart-sales-forecast-mlops

## Workflow for each component

1. Update config.yaml
2. Update schema.yaml
3. Update params.yaml
4. Update the entity
5. Update the configuration manager in src config
6. Update the components
7. Update the pipeline 
8. Update the main.py
9. Update the app.py

# How to run?
### STEPS:

Clone the repository

```bash
https://github.com/HarshVBhatt/walmart-sales-forecast-mlops.git
```
### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n sales-forecast
```

```bash
conda activate sales-forecast
```


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```


### STEP 03- setup aws services

## 1. Login to AWS console.

## 2. Create IAM user for deployment and access key. Note these credentials 

	#Policy:

	1. AmazonEC2ContainerRegistryFullAccess

	2. AmazonEC2FullAccess

	3. AmazonS3FullAccess

## 3. Set up a public s3 bucket with the name "walmart-sales-forecast"

## 4. Configure to read/write to s3
```bash
pip install awscli
aws configure
```

	- Enter the credentials you previously noted.

	- Enter your default region for the region prompt

	- Enter "json" for output prompt

Run the following to ensure s3 access
```bash
aws s3 ls
```

### STEP 04- Download the original data
	Download the original data from - https://kaggle.com/competitions/walmart-recruiting-store-sales-forecasting

	Convert the downloaded .zip files into a single file - raw_data.zip and upload to your github repository (License and competition rule compliance is your responsibility)

	Change the field - "data_ingestion: source_url" om config/config.yaml to reflect the raw_file.zip path


### STEP 05- Run the pipeline locally
```bash
python src/main.py
```

You should see log files being generated showing each step and progress of the pipeline. 

Once the pipeline completes, check s3 folder for successful file uploads



## MLflow

[Documentation](https://mlflow.org/docs/latest/index.html)


##### cmd
- mlflow ui

### dagshub
[dagshub](https://dagshub.com/)

MLFLOW_TRACKING_URI=https://dagshub.com/harshvbhatt/walmart-sales-forecast-mlops.mlflow \
MLFLOW_TRACKING_USERNAME=harshvbhatt \
MLFLOW_TRACKING_PASSWORD=######## \
python script.py

Run this to export as env variables:

```bash

export MLFLOW_TRACKING_URI=https://dagshub.com/harshvbhatt/walmart-sales-forecast-mlops.mlflow

export MLFLOW_TRACKING_USERNAME=harshvbhatt 

export MLFLOW_TRACKING_PASSWORD=########

```



# STEP 06- AWS-CICD-Deployment-with-Github-Actions

## 1. Login to AWS console.

	
## 2. Create ECR repo to store/save docker image
    - Save the URI: 050451357525.dkr.ecr.us-east-2.amazonaws.com/repo-name

	
## 3. Create EC2 machine (Ubuntu) 

## 4. Open EC2 and Install docker in EC2 Machine:
	

	#optional

	sudo apt-get update -y

	sudo apt-get upgrade
	
	#required

	curl -fsSL https://get.docker.com -o get-docker.sh

	sudo sh get-docker.sh

	sudo usermod -aG docker ubuntu

	newgrp docker
	
# 6. Configure EC2 as self-hosted runner:
    setting>actions>runner>new self hosted runner> choose os> then run command one by one


# 7. Setup github secrets:

    AWS_ACCESS_KEY_ID=

    AWS_SECRET_ACCESS_KEY=

    AWS_REGION = us-east-1

    AWS_ECR_LOGIN_URI = demo>>  566373416292.dkr.ecr.ap-south-1.amazonaws.com

    ECR_REPOSITORY_NAME = simple-app

# 8. Configure AWS network and run app

	1. Add an inbound rule with the port 8080 for the instance security group

	2. Open the public IPv4 of the instance xxx.x.x.xx:8080 and the app should run

	3. Click "Run simulation". You should see a plot being generated and updated regularly with the r2 score per batch.