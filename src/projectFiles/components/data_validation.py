from projectFiles import logger
from projectFiles.entity.config_entity import DataValidationConfig
import pandas as pd

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_data(self) -> bool:
        try:
            validation_status = None
            full_status = True
            
            with open(self.config.STATUS_FILE, 'w') as sfile:
                sfile.write("Initializing validation tests")

            for k,v in self.config.data_dirs.items():
                df = pd.read_csv(v)
                df_cols = list(df.columns)
                df_status = True

                schema_cols = self.config.all_schema[k]["COLUMNS"].keys()
                with open(self.config.STATUS_FILE, 'a') as sfile:
                    sfile.write(f"\n\nValidating columns for {k}.csv")
                for col in df_cols:
                    if col not in schema_cols:
                        validation_status = False
                        df_status = False
                        full_status = False
                    else:
                        validation_status = True
                    with open(self.config.STATUS_FILE, 'a') as sfile:
                        sfile.write(f"\nStatus of {v}: {validation_status}")
                with open(self.config.STATUS_FILE, 'a') as sfile:
                    sfile.write(f"\n{k}.csv final validation status: {df_status}")
            
            return full_status
            
        except Exception as e:
            raise e