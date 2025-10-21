import requests
import json

def post_login():
    body = json.dumps({
        "email": "tatarstan@gmail.com",
        "password": "string"
    })
    responce = requests.post(
        'https://mai-tech.ru/api/auth/login/',
        data = body
    )
    print(responce.status_code)
    print(responce.json())

post_login()
