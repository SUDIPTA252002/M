import os
import pandas as pd
import sys
import ast
from src.exception import CustomException
from src.logger import logging
from src.comonents import data_ingestion
from sklearn.feature_extraction.text import TfidfVectorizer
from dataclasses import dataclass

@dataclass
class dataTranformationConfig:
    vectorizer_path=os.path.join("artifacts","vectorizer.pkl")

class data_tranformation():
    def __init__(self):
        self.data_transformation_config=dataTranformationConfig()

    def  convert(self,text):
        genres=[]
        for i in ast.literal_eval(text):
            genres.append(i['name'])

        return genres

    def convert_cast(self,text):
        cast=[]
        count=1
        for i in ast.literal_eval(text):
            #text.replace(" ","")
            cast.append(i["character"])

        return cast

    def convert_crew(self,text):
        L=[]
        for i in ast.literal_eval(text):
            if(i["job"]=="Director"):
                L.append(i["name"])
        return  L

    def initiate_data_transformation(self,raw_data_path):
        movies_df=pd.read_csv(raw_data_path)
        logging.info("READ THE DATA")
        movies=movies_df[["movie_id","title","overview","genres","keywords","cast","crew"]]
        movies["genres"]=movies["genres"].apply(self.convert)


