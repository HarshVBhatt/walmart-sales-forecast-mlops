import numpy as np
import json
import pandas as pd
import pickle
from pathlib import Path
from sklearn.metrics import r2_score
import time
import boto3
from projectFiles import logger
from projectFiles.utils.common import create_directories
import warnings
warnings.filterwarnings("ignore")

def run_sim():
    create_directories(["artifacts/simulation"])
    create_directories(["artifacts/simulation/temp"])

    sim_data = pd.read_csv(Path("artifacts/data_transformation/final_test_data.csv"))

    s3 = boto3.client('s3')

    bucket_name = "walmart-sales-forecast-proj"
    train_data_key = "train_data.csv"
    full_data_key = "updated_data/full_data.csv"
    full_data_path = "artifacts/simulation/temp/full_data.csv"

    s3.download_file(bucket_name, train_data_key, "artifacts/simulation/orig_train_data.csv")
    train_df = pd.read_csv("artifacts/simulation/orig_train_data.csv")
    logger.info("Original data downloaded from s3 bucket")

    dates = np.sort(sim_data["Date"].unique()).tolist()

    with open(Path('artifacts/model_trainer/regressor_pipeline.pkl'), 'rb') as file:
     model = pickle.load(file)

    for date in dates:
        logger.info(f"Running prediction and data updates for {date} batch.")
        batch = sim_data.loc[sim_data["Date"] == date].copy()

        train_df = pd.concat([train_df, batch], axis = 0)
        
        train_df.to_csv(full_data_path, index = False)
        s3.upload_file(full_data_path, bucket_name, full_data_key)
        logger.info("Succesfully updated full data file in s3")

        chunk_path = f"artifacts/simulation/temp/chunk_{date}.csv"
        batch.to_csv(chunk_path, index = False)
        chunk_key = f"updated_data/chunks/chunk_{date}.csv"
        s3.upload_file(chunk_path, bucket_name, chunk_key)
        logger.info(f"Data chunk for {date} added to s3")

        targets = batch["Weekly_Sales"]
        batch.drop(columns = ["Date", "Weekly_Sales"], inplace = True)

        predictions = model.predict(batch)
        r2 = round(r2_score(targets, predictions),4)

        chunk_metrics = {"Samples": len(batch), "r2_score": r2}
        s3.put_object(Body = json.dumps(chunk_metrics), Bucket = bucket_name, Key = f"metrics/{date}/metrics.json")
        logger.info(f"Prediction completed. Metrics logged for {date} batch")
        time.sleep(1)