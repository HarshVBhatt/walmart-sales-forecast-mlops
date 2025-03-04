from projectFiles import logger
from projectFiles.pipeline.stage1_data_ingestion import DataIngestionPipeline
from projectFiles.pipeline.stage2_data_validation import DataValidationPipeline
from projectFiles.pipeline.stage3_data_transformation import DataTransformationPipeline
from projectFiles.pipeline.stage4_model_trainer import ModelTrainerPipeline
from projectFiles.pipeline.stage5_model_evaluation import ModelEvaluationPipeline
from projectFiles.pipeline.simulation import run_sim

def data_ingestion():
    STAGE_NAME = "Data Ingestion"
    try:
        logger.info(f">>>>> Starting stage: {STAGE_NAME} <<<<<")
        pipeline = DataIngestionPipeline()
        pipeline.ingest_data()
        logger.info(f">>>>> Completed stage: {STAGE_NAME} <<<<<")
    except Exception as e:
        raise e

def data_validation():
    STAGE_NAME = "Data Validation"
    try:
        logger.info(f">>>>> Starting stage: {STAGE_NAME} <<<<<")
        obj = DataValidationPipeline()
        obj.run_validation_task()
        logger.info(f">>>>> Completed stage: {STAGE_NAME} <<<<<")
    except Exception as e:
        raise e
    
def data_transformation():
    STAGE_NAME = "Data Transformation"
    try:
        logger.info(f">>>>> Starting stage: {STAGE_NAME} <<<<<")
        obj = DataTransformationPipeline()
        obj.run_transformation()
        logger.info(f">>>>> Completed stage: {STAGE_NAME} <<<<<")
    except Exception as e:
        raise e
    
def model_trainer():
    STAGE_NAME = "Model Trainer"
    try:
        logger.info(f">>>>> Starting stage: {STAGE_NAME} <<<<<")
        obj = ModelTrainerPipeline()
        obj.train_model()
        logger.info(f">>>>> Completed stage: {STAGE_NAME} <<<<<")
    except Exception as e:
        raise e
    
def model_evaluation():
    STAGE_NAME = "Model Evaluation"
    try:
        logger.info(f">>>>> Starting stage: {STAGE_NAME} <<<<<")
        obj = ModelEvaluationPipeline()
        obj.eval_and_log_model()
        logger.info(f">>>>> Completed stage: {STAGE_NAME} <<<<<")
    except Exception as e:
        raise e
    
def run_simulation():
    STAGE_NAME = "SIMULATION"
    try:
        logger.info(f">>>>> Starting stage: {STAGE_NAME} <<<<<")
        run_sim()
        logger.info(f">>>>> Completed stage: {STAGE_NAME} <<<<<")
    except Exception as e:
        raise e

def main():
    data_ingestion()
    data_validation()
    data_transformation()
    model_trainer()
    model_evaluation()
    run_simulation()

if __name__ == "__main__":
    main()