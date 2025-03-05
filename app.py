from flask import Flask, render_template
from flask_socketio import SocketIO
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
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
import io
import base64
warnings.filterwarnings("ignore")


app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def homePage():
    return render_template("index.html")

@socketio.on("run_simulation")
def run_sim():
    logger.info("Starting simulation....")

    plot_dates = []
    r2_scores = []
    app_link = "http://127.0.0.1:5000/"

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
        logger.info("Full data file in s3 updated")

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

        plot_dates.append(str(date)[5:])
        r2_scores.append(r2)

        # socketio.start_background_task(generate_plot_and_emit)
        fig, ax = plt.subplots()
        ax.plot(plot_dates, r2_scores, marker = "o", label = "r2 score")
        ax.set_title("Weekly R2 scores")
        ax.set_xlabel("Date")
        ax.set_ylabel("r2 score")
        ax.tick_params(axis='x', labelrotation=60)
        ax.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format = "png")
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()

        socketio.emit("update_plot", {"image":image_base64})
        logger.info(f"Plot updated at {app_link}")

        time.sleep(1)

# def generate_plot_and_emit():
    
if __name__ == "__main__":
#    socketio.run(app, debug= True, host = "0.0.0.0", port = 8081)
   socketio.run(app, host = "0.0.0.0", port = 8081)