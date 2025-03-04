import os 
from projectFiles import logger
import pandas as pd
import math
from projectFiles.entity.config_entity import DataTransformationConfig
from pathlib import Path
import boto3

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def clean_features_table_basic(self):
        '''
        Load features.csv and perform imputation for Markdown columns, numerical transformation for year and month
        '''
        logger.info("Processing features.csv (stage 1/2 starting)...")
        df = pd.read_csv(self.config.data_dirs["features"])

        # Fill NA with 0
        df[["MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5"]] = df[["MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5"]].fillna(value = 0, axis = 0)

        # Convert year, month to numerical values
        df["Year"] = df["Date"].map(lambda x: x[2:4])
        df["Month"] = df["Date"].map(lambda x: int(x[5:7]))

        df.to_csv(os.path.join(self.config.root_dir, "features_processed.csv"), index = False)
        logger.info("Processing features.csv (stage 1/2 completed). 'Markdown' columns imputed; Date column transformed into numerical types - Year and Month")

    def clean_features_table_cpi_unemp(self):
        '''
        CPI and Unemployment rates are missing for 2013. Impute them using corresponding weekly growth rates for each, from 2012 i.e. previous year
        '''
        logger.info("Processing features.csv (stage 2/2 starting)...")
        features_df = pd.read_csv(os.path.join(self.config.root_dir, "features_processed.csv"))

        # Generate temporary_df to get CPI and Unemployment rate changes
        temp_df = features_df.copy()
        temp_df["next_CPI"] = temp_df["CPI"].shift(periods=-1)
        temp_df["next_UR"] = temp_df["Unemployment"].shift(periods=-1)
        temp_df["CPI_change"] = ((temp_df["next_CPI"] - temp_df["CPI"]) / temp_df["CPI"])
        temp_df["UR_change"] = ((temp_df["next_UR"] - temp_df["Unemployment"]) / temp_df["Unemployment"])

        # Impute CPI and Unemployment Rate with same growth rate as that week of last year
        # # Get uniqe store_week id for 2012
        temp_12 = temp_df.loc[temp_df["Year"] == "12"].copy()
        store_week = []
        store_init = 1
        week_counter = 0

        for i in range(0,len(temp_12)):
            if temp_12.iloc[i]["Store"] == store_init:
                week_counter += 1
                store = str(temp_12.iloc[i]["Store"])
                store_week.append(f"{store}_{str(week_counter)}")
            else:
                store_init += 1
                week_counter = 1
                store = str(temp_12.iloc[i]["Store"])
                store_week.append(f"{store}_{str(week_counter)}")
                
        temp_12["store_week"] = store_week

        # # Get uniqe store_week id for 2013
        features_processed_13 = features_df.loc[features_df["Year"] == "13"].copy()

        store_week = []
        store_init = 1
        week_counter = 0

        for i in range(0,len(features_processed_13)):
            if features_processed_13.iloc[i]["Store"] == store_init:
                week_counter += 1
                store = str(features_processed_13.iloc[i]["Store"])
                store_week.append(f"{store}_{str(week_counter)}")
            else:
                store_init += 1
                week_counter = 1
                store = str(features_processed_13.iloc[i]["Store"])
                store_week.append(f"{store}_{str(week_counter)}")

        features_processed_13["store_week"] = store_week

        # # Join CPI and Unemployment growth rates from 2012 per store per week with corresponding store_week values in 2013
        joint_temp = pd.merge(left = features_processed_13,right = temp_12[["Date", "store_week", "CPI_change", "UR_change"]], on = "store_week", how = "inner")

        # # Impute CPI and Unemp rate values
        joint_temp["CPI"] = joint_temp["CPI"].fillna(0)
        joint_temp["Unemployment"] = joint_temp["Unemployment"].fillna(-100)
        for i,idx in zip(range(0, len(joint_temp)), joint_temp.index):
            if joint_temp.iloc[i]["CPI"] == 0:
                joint_temp.at[idx, "CPI"] = joint_temp.iloc[i-1]["CPI"] * (1+ joint_temp.iloc[i-1]["CPI_change"])
            if joint_temp.iloc[i]["Unemployment"] == -100:
                joint_temp.at[idx, "Unemployment"] = joint_temp.iloc[i-1]["Unemployment"] * (1+ joint_temp.iloc[i-1]["UR_change"])

        # # Clean the joined df
        joint_temp.drop(columns = ["store_week", "Date_y", "CPI_change", "UR_change"], inplace = True)
        joint_temp.rename(columns = {"Date_x":"Date"}, inplace = True)

        # Append imputed rows for 2013 to origianl dataframe
        new_features_df = pd.concat([features_df.loc[features_df["Year"] != "13"], joint_temp], axis = 0)
        new_features_df.reset_index(inplace=True, drop = True)

        new_features_df.to_csv(os.path.join(self.config.root_dir, "features_processed.csv"), index = False)
        logger.info("Processing features.csv (stage 2/2 completed). CPI and Unemployment Rates imputed for year 2013")

    def join_tables(self):
        train_df = pd.read_csv(self.config.data_dirs["train"])
        stores_df = pd.read_csv(self.config.data_dirs["stores"])
        features_df = pd.read_csv(os.path.join(self.config.root_dir, "features_processed.csv"))

        all_join_df = train_df.merge(stores_df, on = "Store", how = "inner")
        all_join_df = all_join_df.merge(features_df, on = ["Store", "Date"], how = "inner")
        all_join_df.drop(columns = ["IsHoliday_y"], inplace = True)
        all_join_df.rename(columns = {"IsHoliday_x": "IsHoliday"}, inplace = True)

        all_join_df.to_csv(os.path.join(self.config.root_dir, "processed_data.csv"), index = False)
        logger.info("Joining all tables completed.")

    def add_features(self):
        '''
        Add temporal, lagged and rolling statistics features
        '''
        df = pd.read_csv(os.path.join(self.config.root_dir, "processed_data.csv"))
        df['Date'] = pd.to_datetime(df['Date'])

        # Temporal features
        df["sin_Month"] = df["Month"].apply(lambda x: math.sin((2 * math.pi * x) / 12))
        df["cos_Month"] = df["Month"].apply(lambda x: math.cos((2 * math.pi * x) / 12)) 
        
        df['Week'] = df['Date'].dt.isocalendar().week
        df["sin_Week"] = df["Week"].apply(lambda x: math.sin((2 * math.pi * x) / 52))
        df["cos_Week"] = df["Week"].apply(lambda x: math.cos((2 * math.pi * x) / 52))

        # Grouped df
        grouped_df = df.groupby(by = ["Store", "Dept"])

        # Lagged features
        df["Sales_Lag_1W"] = grouped_df["Weekly_Sales"].shift(periods=1)
        df["Sales_Lag_2W"] = grouped_df["Weekly_Sales"].shift(periods=2)
        df["Sales_Lag_4W"] = grouped_df["Weekly_Sales"].shift(periods=4)

        # Rolling statistics
        df["Sales_Rolling_Mean_4W"] = grouped_df["Weekly_Sales"].transform(lambda x: x.rolling(window=4).mean())
        df["Sales_Rolling_Std_4W"] = grouped_df["Weekly_Sales"].transform(lambda x: x.rolling(window=4).std())

        df.to_csv(os.path.join(self.config.root_dir, "features_processed.csv"), index = False)
        logger.info("Temporal, lagged and rolling statistic features added.")

    def cat_encoding(self):
        df = pd.read_csv(os.path.join(self.config.root_dir, "features_processed.csv"))

        type_encoded = pd.get_dummies(df["Type"], dtype=int, prefix="Type")
        df = pd.concat([df, type_encoded], axis = 1)
        df.drop(columns = ["Type"], inplace = True)

        df.to_csv(os.path.join(self.config.root_dir, "features_processed.csv"), index = False)
        logger.info("Categorical features encoded.")

    def split_sim_data(self):
        df = pd.read_csv(os.path.join(self.config.root_dir, "features_processed.csv"))
        df_sim= df.loc[df["Date"] >= "2012-07-10"]
        df_train = df.drop(index = df_sim.index)

        df_train.to_csv(os.path.join(self.config.root_dir, "use_for_train_data.csv"), index = False)
        df_sim.to_csv(os.path.join(self.config.root_dir, "use_for_sim_data.csv"), index = False)
        logger.info(f"Data split for training and simulation completed. Using {df_train.shape[0]} samples (till 2012-07-10) for building model. Using {df_sim.shape[0]} samples (from 2012-07-11) for simulation.")

    def split_train_test(self):
        df = pd.read_csv(os.path.join(self.config.root_dir, "use_for_train_data.csv"))
        train_df = df.loc[df["Date"] < "2012-04-01"]
        test_df = df.drop(index = train_df.index)
        
        train_df.to_csv(os.path.join(self.config.root_dir, "final_train_data.csv"), index = False)
        test_df.to_csv(os.path.join(self.config.root_dir, "final_test_data.csv"), index = False)
        logger.info(f"Further split of model building data for training ({train_df.shape[0]} samples) and testing ({test_df.shape[0]} samples) completed")

    def push_to_s3(self):
        s3 = boto3.client('s3')
        bucket_name = "walmart-sales-forecast-proj"
        object_path = Path("artifacts/data_transformation/final_train_data.csv")
        key = "train_data.csv"

        try:
            s3.upload_file(object_path, bucket_name, key)
            logger.info(f"final_train_data.csv uploaded successfully to s3 bucket '{bucket_name}' as '{key}'")
        except Exception as e:
            print(f"Error uploading file: {e}")