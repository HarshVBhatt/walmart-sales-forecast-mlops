import pickle
import pandas as pd
from pathlib import Path
from lightgbm import LGBMRegressor

class PredictionPipeline:
    def __init__(self):
        with open(Path('artifacts/model_trainer/regressor_pipeline.pkl'), 'rb') as file:
            self.model = pickle.load(file)

    def predict(self, data):
        prediction = self.model.predict(data)
        return prediction
