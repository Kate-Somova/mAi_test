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
    body = {
        "email": "testsssdsdd@example.com",
        "password": "string",
        "first_name": "Kates",
        "last_name": "test",
        "timezone": "string",
        "organization": "string",
        "phone_number": "+7(926)777-77-79",
        "phone_country_code": "string",
        "lang": "str",
        "rate": "ele"
    }
    responce = requests.post(
        'https://mai-tech.ru/api/auth/signup/',
        json=body
    )
    assert responce.status_code == 200
    pprint(responce.json())
    # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjE1OTI1MzEsImlhdCI6MTc2MTU1NjUzMSwic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJzdWIiOiJ0ZXN0c3NzZHNkZEBleGFtcGxlLmNvbSJ9.7Y7Aj4_ZZjgfoOpBdTDQAu3t1DmlhmWRR3h81YvWFTA
