from dataclasses import dataclass, field
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    all_schema: dict
    data_dirs: dict = field(default_factory= lambda: {
        'features': Path,
        'stores': Path,
        'train': Path,
        'test': Path
    })

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_dirs: dict = field(default_factory= lambda: {
        'features': Path,
        'stores': Path,
        'train': Path,
        'test': Path
    })

@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path 
    pipeline_name: str
    model_instance_name: str
    n_estimators: int
    learning_rate: float
    target_column: str

@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    pipeline_path: Path 
    model_instance_path: Path
    all_params: dict
    target_column: str
    metrics_file_name: Path
    mlflow_uri: str