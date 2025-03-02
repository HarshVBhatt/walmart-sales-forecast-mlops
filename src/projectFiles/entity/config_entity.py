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