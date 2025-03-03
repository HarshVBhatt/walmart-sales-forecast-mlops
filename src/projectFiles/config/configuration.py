from projectFiles.constants import *
from projectFiles.utils.common import read_yaml, create_directories
from projectFiles.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig

class ConfigurationManager:
    def __init__(self, config_filepath = CONFIG_FILE_PATH, params_filepath = PARAMS_FILE_PATH, schema_filepath = SCHEMA_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir = config.root_dir,
            source_URL = config.source_URL,
            local_data_file = config.local_data_file,
            unzip_dir = config.unzip_dir
        )

        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema
        
        data_files_dirs = {}
        for k,v in config.data_dirs.items():
            data_files_dirs[k] = v

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir = config.root_dir,
            STATUS_FILE = config.STATUS_FILE,
            all_schema = schema,
            data_dirs = data_files_dirs
        )

        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation

        data_files_dirs = {}
        for k,v in config.data_dirs.items():
            data_files_dirs[k] = v

        create_directories([config.root_dir])
        data_transformation_config = DataTransformationConfig(
            root_dir = config.root_dir,
            data_dirs = data_files_dirs
        )

        return data_transformation_config
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        schema = self.schema
        params = self.params.LGBMRegressor

        create_directories([config.root_dir])
        
        model_trainer_config = ModelTrainerConfig(
            root_dir = config.root_dir,
            train_data_path = config.train_data_path,
            test_data_path = config.test_data_path,
            pipeline_name = config.pipeline_name,
            model_instance_name = config.model_instance_name,
            n_estimators = params.n_estimators,
            learning_rate = params.learning_rate,
            target_column = schema.TARGET_COLUMN.name
        )

        return model_trainer_config
    
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        params = self.params.LGBMRegressor
        schema = self.schema

        create_directories([config.root_dir])
        
        model_evaluation_config = ModelEvaluationConfig(
            root_dir = config.root_dir,
            test_data_path = config.test_data_path,
            pipeline_path = config.pipeline_path,
            model_instance_path = config.model_instance_path,
            all_params = params,
            metrics_file_name = config.metrics_file_name,
            target_column = schema.TARGET_COLUMN.name,
            mlflow_uri = "https://dagshub.com/harshvbhatt/walmart-sales-forecast-mlops.mlflow"
        )

        return model_evaluation_config