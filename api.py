import requests
import json

def get_all_posts():
    responce = requests.get('https://jsonplaceholder.typicode.com/posts').json()
    for x in responce:
        print(x)

def get_one_post():
    responce = requests.get('https://jsonplaceholder.typicode.com/posts/42').json()
    print(responce)

def post_new_post():
    headers = {
        'Content-type': 'application/json; charset=UTF-8'
    }
    body = json.dumps({
         "title": "foo",
         "body": "bar",
         "userId": 1
    })
    responce = requests.post(
        'https://jsonplaceholder.typicode.com/posts',
        data = body,
        headers = headers
    )
    print(responce.json())
    print(responce.status_code)

def update_post():
    headers = {
        'Content-type': 'application/json; charset=UTF-8'
    }
    body = json.dumps({
        "title": "fool",
        "body": "bark",
        "userId": 1
    })
    responce = requests.put(
        'https://jsonplaceholder.typicode.com/posts/42',
        data=body,
        headers=headers
    )
    print(responce.json())
    print(responce.status_code)

def patch_post():
    headers = {
        'Content-type': 'application/json; charset=UTF-8'
    }
    body = json.dumps({
        "title": "fool",
        "userId": 1
    })
    responce = requests.patch(
        'https://jsonplaceholder.typicode.com/posts/42',
        data=body,
        headers=headers
    )
    print(responce.json())
    print(responce.status_code)

def delete_post():
    responce = requests.delete('https://jsonplaceholder.typicode.com/posts/42')
    print(responce.text)
    print(responce.status_code)

patch_post()