from src.projectFiles import logger
from src.projectFiles.pipeline.stage_data_ingestion import DataIngestionPipeline

def main():
    try:
        pipeline = DataIngestionPipeline
        pipeline.ingest_data()
    except Exception as e:
        raise e
    
if __name__ == "__main__":
    main()