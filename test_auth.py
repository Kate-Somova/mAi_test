from pprint import pprint

import requests
import json

def test_post_token():
    body = json.dumps({
        "email": "tatarstan@gmail.com",
        "password": "string"
    })
    responce = requests.post(
        'https://mai-tech.ru/api/auth/login/',
        data = body
    )
    my_token = responce['access_token']
    assert responce.status_code == 200
    pprint(responce.json())

