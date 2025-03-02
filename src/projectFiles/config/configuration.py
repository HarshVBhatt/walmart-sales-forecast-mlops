from projectFiles.constants import *
from projectFiles.utils.common import read_yaml, create_directories
from projectFiles.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig

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