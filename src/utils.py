import os
import sys
from src.exception import CustomException
from src.logger import logging
import dill


def save_object(filepath,obj):

    try:
        dir_path=os.path.dirname(filepath)
        os.makedirs(dir_path,exist_ok=True)
        with open(filepath,"wb") as fileobj:
            dill.dump(obj,fileobj)
    except Exception as e:
        raise CustomException(e,sys)