import pandas as pd
from sklearn.metrics import root_mean_squared_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import pickle
from projectFiles.entity.config_entity import ModelEvaluationConfig
from projectFiles.utils.common import save_json
from pathlib import Path
from projectFiles import logger

class ModelEvaluation:
    def __init__(self, config = ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, pred):
        rmse = root_mean_squared_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, r2
    
    def log_in_mlflow(self):
        target_col = self.config.target_column
        test_df = pd.read_csv(self.config.test_data_path)
        with open(self.config.pipeline_path, 'rb') as file:
            regressor_pipeline = pickle.load(file)
        with open(self.config.model_instance_path, 'rb') as file:
            model_instance = pickle.load(file)   

        test_df.drop(columns=["Date"], inplace = True)
        test_x = test_df.drop(columns=target_col)
        test_y = test_df[target_col]

        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            prediction = regressor_pipeline.predict(test_x)
            
            (rmse, r2) = self.eval_metrics(test_y, prediction)

            scores = {"rmse":rmse, "r2":r2}
            save_json(path = Path(self.config.metrics_file_name), data = scores)
            logger.info(f"Metrics saved at {self.config.metrics_file_name}")

            mlflow.log_params(self.config.all_params)

            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)
            logger.info(f"Metrics logged in MLflow")

            # Save Pipeline
            if tracking_url_type_store != "file":
                mlflow.sklearn.log_model(regressor_pipeline, "model", registered_model_name="LGBMRegressorPipeline")
            else:
                mlflow.sklearn.log_model(regressor_pipeline, "model")

            # # Save Model Instance
            # if tracking_url_type_store != "file":
            #     mlflow.sklearn.log_model(model_instance, "model", registered_model_name="LGBMRegressor") 

            # else:
            #     mlflow.sklearn.log_model(model_instance, "model")

            logger.info("Model successfully registered on MLFlow")