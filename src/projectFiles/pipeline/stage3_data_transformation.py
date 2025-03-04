from projectFiles.config.configuration import ConfigurationManager
from projectFiles.components.data_transformation import DataTransformation
from projectFiles import logger
from pathlib import Path

STAGE_NAME = "Data Transformation"

class DataTransformationPipeline:
    def __init__(self):
        pass

    def run_transformation(self):
        try:
            with open(Path("artifacts/data_validation/status.txt"), "r") as f:
                status = f.read()[-4:]
            
            if status == "True":
                config = ConfigurationManager()
                data_transformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(config = data_transformation_config)
                data_transformation.clean_features_table_basic()
                data_transformation.clean_features_table_cpi_unemp()
                data_transformation.join_tables()
                data_transformation.add_features()
                data_transformation.cat_encoding()
                data_transformation.split_sim_data()
                data_transformation.split_train_test()
                data_transformation.push_to_s3()

            else:
                raise Exception("Data schema is invalid. Refer artifacts/data_validation/status.txt for detailed information")
        except Exception as e:
            print(e)

# def main():
#     try:
#         logger.info(f">>>>> Starting stage: {STAGE_NAME} <<<<<")
#         obj = DataTransformationPipeline()
#         obj.run_transformation()
#         logger.info(f">>>>> Completed stage: {STAGE_NAME} <<<<<")
#     except Exception as e:
#         raise e
    
# if __name__ == "__main__":
#     main()