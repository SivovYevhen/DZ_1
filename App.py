import requests
import json
import datetime
import os

from Config import Config
from datetime import timedelta
from requests.exceptions import ConnectionError

def app_t():
    # Получение авторизации-------------------------------
    config_f = Config("./config.yaml")
    config =config_f.get_config()
    e = 0
    try:
        r = requests.post(config['url'] + '/' + config['endpoint_A']
                           , data=json.dumps({"username": config['username'], "password": config['password']})
                           , headers={"content-type": "application/json"}    )
        at = r.json()["access_token"]
    except ConnectionError:
        e=1
        print('Error taking token')

    return 0 if e==1 else at

def app( process_date, at ):
    # Получение информации-------------------------------
    config_f = Config("./config.yaml")
    config =config_f.get_config()

    dt = process_date
    print(dt)

    url = config['url'] + '/' + config['endpoint_S']
    headers = {"Authorization": "JWT " + at , "content-type": "application/json"}
    data = {"date": str(dt)}

    try:
        r1 = requests.get(url, headers = headers , data =json.dumps(data) )
    except ConnectionError:
        print('Error extraction data')

    # Сохранение информации-------------------------------
    path_to_dir = os.path.join('.','data',config['endpoint_S'],str(dt1))
    os.makedirs(path_to_dir, exist_ok=True)

    with open(path_to_dir +'/'+ config['file_name'],'w') as json_file:
        json.dump(r1.json() , json_file)

if __name__ == "__main__":
    dt = datetime.date(2021, 5, 1)
    i = 0
    while i < 5:
        # Получение токена
        t = app_t()
        if t == 0: break

        # Получение информации
        dt1 = dt + timedelta(days=i)
        app(dt1 ,t )
        i = i + 1