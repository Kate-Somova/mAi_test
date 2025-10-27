import pytest_check as check
import requests

from test_auth import get_token


# def test_get_pub_list():
#    my_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjE1NzUzOTAsImlhdCI6MTc2MTUzOTM5MCwic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJzdWIiOiJ0YXRhcnN0YW5AZ21haWwuY29tIn0.F9CpP-hMPulApA6GahylbtiaH6rXB8rn69royALh7Bk'
#    headers = {
#        'Authorization': f'Bearer {my_token}'
#    }
#    responce = requests.get(
#        'https://mai-tech.ru/api/pubs/',
#        headers=headers).json()
#    print(responce)
# Не отрабатывает, тайм-аут более 10 секунд


def test_get_pub_detail(get_token):
    headers = {
        'Authorization': f"Bearer {get_token}"
    }
    pub_id = 101
    responce = requests.get(
        f'https://mai-tech.ru/api/pubs/{pub_id}',
        headers=headers).json()
    #  pprint(responce)
    # {'id': 101, 'theme_id': 3875813, 'title': None, 'text': None, 'highlights': None, 'is_main': False, 'trusted': True, 'url': None, 'source': None, 'force': None, 'lang': None, 'entities': {}, 'media': None, 'date': None, 'created_at': '2023-07-12T18:07:42.894142', 'updated_at': '2023-07-12T18:07:42.894142'}
    with check.check():
        assert responce['theme_id'] == 3875813
        assert responce['is_main'] is False
    print('okey')
