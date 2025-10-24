from pprint import pprint
from tabnanny import check
import requests


def test_get_pub_list():
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjEzMzIzNjcsImlhdCI6MTc2MTI5NjM2Nywic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJzdWIiOiJ0YXRhcnN0YW5AZ21haWwuY29tIn0.T8UneVmnMNqCmcSp4f4hfLz2AuWaWE8zRX9NoRDhZOs'
    }
    responce = requests.get(
        'https://mai-tech.ru/api/pubs/',
        headers=headers).json()
    print(responce)
    # Не отрабатывает, тайм-аут более 10 секунд


def test_get_pub_detail():
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjEzMzIzNjcsImlhdCI6MTc2MTI5NjM2Nywic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJzdWIiOiJ0YXRhcnN0YW5AZ21haWwuY29tIn0.T8UneVmnMNqCmcSp4f4hfLz2AuWaWE8zRX9NoRDhZOs'
    }
    responce = requests.get(
        'https://mai-tech.ru/api/pubs/101/',
        headers=headers).json()
    pprint(responce)
    # {'id': 101, 'theme_id': 3875813, 'title': None, 'text': None, 'highlights': None, 'is_main': False, 'trusted': True, 'url': None, 'source': None, 'force': None, 'lang': None, 'entities': {}, 'media': None, 'date': None, 'created_at': '2023-07-12T18:07:42.894142', 'updated_at': '2023-07-12T18:07:42.894142'}
    with check:
        assert responce['theme_id'] == 38758
        assert responce['is_main'] is False
    print('okey')
