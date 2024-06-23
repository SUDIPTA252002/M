import pandas as pd
import sys
import os
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass

@dataclass
class Data_Ingestion_Config:
    raw_data_path=os.path.join("artifacts","raw_data.csv")

class Data_Ingestion:
    def __init__(self):
        self.data_ingestion_config=Data_Ingestion_Config()
    def initiate_data_ingestion(self):
        try:
            movies_path = 'data/movies.csv'
            credits_path = 'data/credits.csv'
            
            # Read the datasets
            movies_df = pd.read_csv(movies_path)
            credits_df = pd.read_csv(credits_path)

            # Example: Merge the datasets if needed (this step depends on your specific use case)
            movies_df= movies_df.merge(credits_df,on='title')
            logging.info("LOADING THE RAW DATA")
            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_data_path),exist_ok=True)
            movies_df.to_csv(self.data_ingestion_config.raw_data_path,index=False,header=True)
            logging.info("DATA INGESTION IS COMPLETED")
            return(
                self.data_ingestion_config.raw_data_path
            )

        except Exception as e:
            raise CustomException(e,sys)

if __name__=="__main__":
    obj=Data_Ingestion()
    test_data_path=obj.initiate_data_ingestion()