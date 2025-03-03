import pandas as pd
import pickle
from lightgbm import LGBMRegressor
from sklearn.preprocessing import MinMaxScaler 
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from projectFiles import logger
from projectFiles.entity.config_entity import ModelTrainerConfig
import os 

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        target_col = self.config.target_column

        train_df = pd.read_csv(self.config.train_data_path)
        test_df = pd.read_csv(self.config.test_data_path)

        train_df.drop(columns=["Date"], inplace=True)
        test_df.drop(columns=["Date"], inplace = True)

        categorical_cols = [c for c in train_df.columns if train_df[c].dtype in [object]]
        numerical_cols = [c for c in train_df.columns if train_df[c].dtype in [float, int] and c != target_col]
        cycl_num_cols = [c for c in train_df.columns if ("sin" in str(c)) or ("cos" in str(c))]

        train_x = train_df.drop(columns=target_col)
        train_y = train_df[target_col]
        test_x = test_df.drop(columns=target_col)
        test_y = test_df[target_col]

        pipeline = make_pipeline(ColumnTransformer([("num", MinMaxScaler(), [c for c in numerical_cols if c not in cycl_num_cols])]),
                                 LGBMRegressor(n_jobs=-1, random_state=100, n_estimators = self.config.n_estimators, learning_rate = self.config.learning_rate))
        regressor = pipeline.fit(train_x, train_y)
        model_instance = regressor.named_steps["lgbmregressor"]

        pickle.dump(regressor, open(os.path.join(self.config.root_dir, self.config.pipeline_name), 'wb'))
        logger.info(f"Training Pipeline successfully saved at {self.config.root_dir}/{self.config.pipeline_name}")
        pickle.dump(model_instance, open(os.path.join(self.config.root_dir, self.config.model_instance_name), 'wb'))
        logger.info(f"Model Instance successfully saved at {self.config.root_dir}/{self.config.model_instance_name}")
    