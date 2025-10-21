import requests
import json


def get_pub_list():
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjEwNTAxMjksImlhdCI6MTc2MTAxNDEyOSwic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJzdWIiOiJ0YXRhcnN0YW5AZ21haWwuY29tIn0.gh5kTMMr3O5vKRk_JgjjiMciJ1-mmBSObKloKTW7j3I'
    }
    responce = requests.get(
        'https://mai-tech.ru/api/pubs/',
        headers=headers).json()
    print(responce)


get_pub_list()
