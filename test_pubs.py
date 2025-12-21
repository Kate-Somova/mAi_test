import pytest_check as check
import requests
from pytest import fixture


@fixture()
def get_token():
    body = {
        "email": "tatarstan@gmail.com",
        "password": "string"
    }
    responce = requests.post(
        'https://mai-tech.ru/api/auth/login/',
        json=body
    )
    # print('Статус-код:', responce.status_code)
    print('Ответ:', responce.text)
    data = responce.json()
    return data.get('access_token')


def test_get_pub_detail(get_token):
    headers = {
        'Authorization': f"Bearer {get_token}"
    }
    pub_id = 101
    responce = requests.get(
        f'https://mai-tech.ru/api/pubs/{pub_id}',
        headers=headers).json()
    # pprint(responce)
    with check.check():
        assert responce['theme_id'] == 3875813
        assert responce['is_main'] is False
    print('okey')
