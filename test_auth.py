import requests
from pytest_check import check

import config


# def test_get_token():
#    body = json.dumps({
#        "email": "tatarstan@gmail.com",
#        "password": "string"
#    })
#    responce = requests.post(
#        'https://mai-tech.ru/api/auth/login/',
#        data=body
#    )
#    assert responce.status_code == 200
#    pprint(responce.json())


def test_signup_200():
    body = {
        "email": "tesdaad@example.com",
        "password": "string",
        "first_name": "Kate",
        "last_name": "Somova",
        "timezone": "+3",
        "organization": "OON",
        "phone_number": "+7(926)777-77-79",
        "phone_country_code": "+7",
        "lang": "RU",
        "rate": "org"
    }
    responce = requests.post(
        'https://mai-tech.ru/api/auth/signup/',
        json=body
    )
    assert responce.status_code == 200
    data = responce.json()
    config.ACCESS_TOKEN = data['access_token']
    config.USER_DATA = body


def test_new_profile_check():
    headers = {
        'Authorization': f"Bearer {config.ACCESS_TOKEN}"
    }
    responce = requests.get(
        f'https://mai-tech.ru/api/profile',
        headers=headers)
    data = responce.json()
    with check.check():
        assert data['first_name'] == config.USER_DATA['first_name']
        assert data['organization'] == config.USER_DATA['organization']
        assert data['email'] == config.USER_DATA['email']
        assert data['phone_number'] == config.USER_DATA['phone_number']
        assert data['phone_country_code'] == config.USER_DATA['phone_country_code']
        assert data['timezone'] == config.USER_DATA['timezone']
        assert data['rate'] == config.USER_DATA['rate']
        assert data['lang'] == config.USER_DATA['lang']
