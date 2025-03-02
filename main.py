from src.projectFiles import logger
from projectFiles.pipeline.stage1_data_ingestion import DataIngestionPipeline
from projectFiles.pipeline.stage2_data_validation import DataValidationPipeline

def data_ingestion():
    STAGE_NAME = "Data Ingestion"
    try:
        logger.info(f">>>>> Starting stage: {STAGE_NAME} <<<<<")
        pipeline = DataIngestionPipeline
        pipeline.ingest_data()
        logger.info(f">>>>> Completed stage: {STAGE_NAME} <<<<<")
    except Exception as e:
        raise e

def data_validation():
    STAGE_NAME = "Data Validation"
    try:
        logger.info(f">>>>> Starting stage: {STAGE_NAME} <<<<<")
        obj = DataValidationPipeline
        obj.run_validation_task()
        logger.info(f">>>>> Completed stage: {STAGE_NAME} <<<<<")
    except Exception as e:
        raise e

def main():
    data_ingestion()
    data_validation()
    
if __name__ == "__main__":
    main()