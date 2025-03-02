from projectFiles.config.configuration import ConfigurationManager
from projectFiles.components.data_validation import DataValidation
from projectFiles import logger

STAGE_NAME = "Data Validation"

class DataValidationPipeline:
    def __init__(self):
        pass

    def run_validation_task(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config = data_validation_config)
        data_validation.validate_data()


# def main():
#     try:
#         logger.info(f">>>>> Starting stage: {STAGE_NAME} <<<<<")
#         obj = DataValidationPipeline
#         obj.run_validation_task()
#         logger.info(f">>>>> Completed stage: {STAGE_NAME} <<<<<")
#     except Exception as e:
#         raise e
    
# if __name__ == "__main__":
#     main()