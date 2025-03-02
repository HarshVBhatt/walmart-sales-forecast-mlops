from projectFiles.config.configuration import ConfigurationManager
from projectFiles.components.data_ingestion import DataIngestion
from projectFiles import logger

STAGE_NAME = "Data Ingestion"

class DataIngestionPipeline:
    def __init__(self):
        pass

    def ingest_data(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config = data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip()

# def main():
#     try:
#         logger.info(f">>>>> Starting stage: {STAGE_NAME} <<<<<")
#         obj = DataIngestionPipeline
#         obj.ingest_data()
#         logger.info(f">>>>> Completed stage: {STAGE_NAME} <<<<<")
#     except Exception as e:
#         raise e
    
# if __name__ == "__main__":
#     main()