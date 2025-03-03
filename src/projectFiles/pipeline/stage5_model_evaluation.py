from projectFiles.config.configuration import ConfigurationManager
from projectFiles.components.model_evaluation import ModelEvaluation
from projectFiles import logger
from pathlib import Path

STAGE_NAME = "Model Evaluation"

class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def eval_and_log_model(self):
        try:
            config = ConfigurationManager()
            model_evaluation_config = config.get_model_evaluation_config()
            model_evaluation = ModelEvaluation(config = model_evaluation_config)
            model_evaluation.log_in_mlflow()
        except Exception as e:
            raise e

# def main():
#     try:
#         logger.info(f">>>>> Starting stage: {STAGE_NAME} <<<<<")
#         obj = ModelEvaluationPipeline()
#         obj.train_model()
#         logger.info(f">>>>> Completed stage: {STAGE_NAME} <<<<<")
#     except Exception as e:
#         raise e
    
# if __name__ == "__main__":
#     main()