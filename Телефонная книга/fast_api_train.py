### 1
# import requests
# from datetime import datetime,timedelta
# import json
# from IPython.display import Image
# import os
#
# SERVER_URL = 'https://jservice.io/api/random?count=1'
# response = requests.get(SERVER_URL)
#
# print(dir(response))
# print(response.status_code)
# print(response.text)

### 2
# from fastapi import FastAPI
#
# app = FastAPI()
#
# @app.get("/")
# async def root():
#     return {"message":"Hello World!"}

### 3

from fastapi import FastAPI
from typing import Optional
import pandas as pd
import json
import numpy as np
from data_requests import *

app = FastAPI()
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

@app.get("/")
async def root():
    return "Phonebook"

@app.post("/add-user")
async def add_user(parameters: User):
# Считываем/Создаем телефонный справочник
    try:
        df_phonebook = pd.read_csv('df.csv')
    except:
        df_phonebook = pd.DataFrame(columns = ['Firstname','Lastname','Phone number','Age'])
        # df_phonebook['Phone number'] = df_phonebook['Phone number'].astype(str)

    user_dict = {}
    user_dict['Firstname'] = parameters.first_name
    user_dict['Lastname'] = parameters.last_name
    user_dict['Phone number'] = parameters.phone_number

    print(f'Firstname:{parameters.first_name}')
    print(f'Lastname:{parameters.last_name}')
    print(f'Phone number:{parameters.phone_number}')
    if parameters.age:
        print(f'Age:{parameters.age}')
        user_dict['Age'] = parameters.age
    else:
        user_dict['Age'] = 'None'

    print(user_dict)
    df_temp = pd.DataFrame([user_dict])
    print(df_phonebook)
    print(df_temp)
    df_phonebook = pd.concat([df_phonebook,df_temp])
    df_phonebook.to_csv('df.csv')
    return 'user is added'

@app.get("/get-user")
async def get_user(last_name:str):
    try:
        df_phonebook = pd.read_csv('df.csv')
    except:
        df_phonebook = pd.DataFrame(columns=['Firstname', 'Lastname', 'Phone number', 'Age'])

    # Пытаемся найти пользователя
    df_temp = df_phonebook[df_phonebook['Lastname']==last_name]
    if df_temp.empty:
        return 'There is no such user'
    print('Телефон',dict(df_temp.iloc[0]))
    return json.dumps(dict({'Phone number':df_temp.iloc[0]['Phone number']}),cls=NpEncoder)

