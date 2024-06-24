import os
import pandas as pd
import sys
import ast
from src.exception import CustomException
from src.logger import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from dataclasses import dataclass
from src.utils import save_object

@dataclass
class dataTranformationConfig:
    vectorizer_path=os.path.join("artifacts","vectorizer.pkl")
    new_path=os.path.join("aritfacts","new_data.csv")

class data_transformation():
    def __init__(self):
        self.data_transformation_config=dataTranformationConfig()

    def get_data_transformer(self):
        obj=TfidfVectorizer(max_features=5000,stop_words="english")
        return obj

    def  convert(self,text):
        try:
            genres=[]
            for i in ast.literal_eval(text):
                genres.append(i['name'])

            return genres
        except Exception as e:
            raise CustomException(e,sys)

    def convert_cast(self,text):
        try:
            cast=[]
            count=1
            for i in ast.literal_eval(text):
                #text.replace(" ","")
                cast.append(i["character"])

            return cast
        except Exception as e:
            raise CustomException(e,sys)

    def convert_crew(self,text):
        try:
            L=[]
            for i in ast.literal_eval(text):
                if(i["job"]=="Director"):
                    L.append(i["name"])
            return  L
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self, raw_data_path):
        try:
            movies_df = pd.read_csv(raw_data_path)
            logging.info("READ THE DATA")
            
            movies = movies_df[["movie_id", "title", "overview", "genres", "keywords", "cast", "crew"]]
            
            movies.loc[:, "genres"] = movies["genres"].apply(self.convert)
            movies.loc[:, "keywords"] = movies["keywords"].apply(self.convert)
            movies.loc[:, "cast"] = movies["cast"].apply(self.convert_cast)
            movies.loc[:, "crew"] = movies["crew"].apply(self.convert_crew)
            
            movies["overview"] = movies["overview"].fillna("")  # Handle NaN values
            movies["overview"] = movies["overview"].apply(lambda x: x.split() if isinstance(x, str) else [])
            
            movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
            new = movies.drop(columns=['overview', 'genres', 'keywords', 'cast', 'crew'])

            new['tags'] = new['tags'].apply(lambda x: " ".join(x))

            os.makedirs(os.path.dirname(self.data_transformation_config.new_path),exist_ok=True)
            new.to_csv(self.data_transformation_config.new_path,index=False,header=True)
            new.head(2)
            
            logging.info("FEATURE SELECTION COMPLETED")
            
            vectorizer = self.get_data_transformer()
            vector = vectorizer.fit_transform(new['tags']).toarray()
            
            logging.info("SAVING THE VECTORIZER")
            
            save_object(
                filepath=self.data_transformation_config.vectorizer_path,
                obj=vectorizer
            )
            
            return vector, self.data_transformation_config.vectorizer_path

        except Exception as e:
            raise CustomException(e, sys)


        



