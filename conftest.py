import os
import pytest
import requests
import config


@pytest.fixture
# фикстура на получение токена
def get_token():
    # 1. Получаем данные из .env
    email = os.getenv("main_user_email")
    password = os.getenv("main_user_password")
    BASE_URL = os.getenv("BASE_URL")

    # 2. Логинимся
    response = requests.post(
        f'{BASE_URL}/auth/login/',
        json={"email": email, "password": password}
    )
    assert response.status_code == 200, f"Login failed: {response.status_code}"
    token = response.json()["access_token"]
    headers = {'Authorization': f'Bearer {token}'}

    # Возвращаем
    yield token

    # выходим из аккаунта
    requests.post(
        f'{BASE_URL}/auth/logout/',
        headers=headers
    )


@pytest.fixture
def new_user_with_delete():
    # фикстура на создание нового пользователя (создание и удаление)
    body = config.body_new_user.copy()
    BASE_URL = os.getenv("BASE_URL")
    response = requests.post(
        f'{BASE_URL}/auth/signup/',
        json=body
    )

    data = response.json()
    access_token = data['access_token']

    profile_response = requests.get(
        f'{BASE_URL}/profile',
        headers={'Authorization': f"Bearer {access_token}"}
    )

    uid = profile_response.json()['uid']

    yield {
        "access_token": access_token,
        "uid": uid,
        "user_data": body,
        "response_data": data
    }

    requests.delete(
        f'{BASE_URL}/profile/total/{uid}',
        headers={'Authorization': f"Bearer {access_token}"}
    )
