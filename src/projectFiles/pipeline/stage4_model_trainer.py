from projectFiles.config.configuration import ConfigurationManager
from projectFiles.components.model_trainer import ModelTrainer
from projectFiles import logger
from pathlib import Path

STAGE_NAME = "Model Trainer"

class ModelTrainerPipeline:
    def __init__(self):
        pass

    def train_model(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config = model_trainer_config)
        model_trainer.train()

# def main():
#     try:
#         logger.info(f">>>>> Starting stage: {STAGE_NAME} <<<<<")
#         obj = ModelTrainerPipeline()
#         obj.train_model()
#         logger.info(f">>>>> Completed stage: {STAGE_NAME} <<<<<")
#     except Exception as e:
#         raise e
    
# if __name__ == "__main__":
#     main()