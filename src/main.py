from projectFiles import logger
from projectFiles.pipeline.stage_data_ingestion import DataIngestionPipeline

def main():
    try:
        STAGE_NAME = "Data Ingestion"
        logger.info(f">>>>> Starting stage: {STAGE_NAME} <<<<<")
        pipeline = DataIngestionPipeline()
        pipeline.ingest_data()
        logger.info(f">>>>> Completed stage: {STAGE_NAME} <<<<<")
    except Exception as e:
        raise e
    
if __name__ == "__main__":
    main()