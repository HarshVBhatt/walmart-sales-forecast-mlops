import os
import urllib.request as request
import zipfile
from projectFiles import logger
from projectFiles.utils.common import get_size
from pathlib import Path
from projectFiles.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(url = self.config.source_URL, filename = self.config.local_data_file)
            logger.info(f"{filename} downloaded with the following info: {headers}")
        else:
            logger.info(f"File already exists with size: {get_size(Path(self.config.local_data_file))}")
    
    def extract_zip(self):
        unzip_path = self.config.unzip_dir

        os.makedirs(unzip_path, exist_ok=True)

        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)