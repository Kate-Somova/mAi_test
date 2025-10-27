import json
from pprint import pprint

import pytest
import requests


@pytest.fixture()
def get_token():
    body = json.dumps({
        "email": "tatarstan@gmail.com",
        "password": "string"
    })
    responce = requests.post(
        'https://mai-tech.ru/api/auth/login/',
        data=body
    ).json()
    return responce['access_token']


def test_get_token():
    body = json.dumps({
        "email": "tatarstan@gmail.com",
        "password": "string"
    })
    responce = requests.post(
        'https://mai-tech.ru/api/auth/login/',
        data=body
    )
    assert responce.status_code == 200
    pprint(responce.json())


def test_signup():
    body = json.dumps({
        "email": "testsssdd@example.com",
        "password": "string",
        "first_name": "Kates",
        "last_name": "test",
        "timezone": "string",
        "organization": "string",
        "phone_number": "+7(926)777-77-79",
        "phone_country_code": "string",
        "lang": "str",
        "rate": "ele"
    })
    responce = requests.post(
        'https://mai-tech.ru/api/auth/signup/',
        data=body
    )
    assert responce.status_code == 200
    pprint(responce.json())
