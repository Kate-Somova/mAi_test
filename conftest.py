import os
import pytest
import requests
import config
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
# фикстура на получение токена
def get_token():
    # Получаем данные из .env
    BASE_URL = os.getenv("BASE_URL")

    # Логинимся
    response = requests.post(
        f'{BASE_URL}/auth/login/',
        json={"email": os.getenv("MAIN_USER_EMAIL"), "password": os.getenv("MAIN_USER_PASSWORD")},
        timeout=10
    )
    # Если статус не 200 - возвращаем ошибку
    if response.status_code != 200:
        yield {
            'success': False,
            'error': f"Ошибка {response.status_code}: {response.text}"
        }
        return

    # Получаем токен
    access_token = response.json()['access_token']

    # Возвращаем токен тесту
    yield {
            'success': True,
            'access_token': access_token
        }

    # выходим из аккаунта
    try:
        headers = {'Authorization': f'Bearer {access_token}'}
        requests.post(
            f'{BASE_URL}/auth/logout/',
            headers=headers,
            timeout=10
        )
    except Exception as e:
        print(f"Не удалось выйти из аккаунта: {e}")


@pytest.fixture()
# фикстура на создание и удаление нового пользователя
def new_user_with_delete():
    try:
        BASE_URL = os.getenv("BASE_URL")
        response = requests.post(
            f'{BASE_URL}/auth/signup/',
            json=config.body_new_user
        )
        if response.status_code != 200:
            yield {
                'success': False,
                'error': response.text,
                'status': response.status_code
            }
            return
        data = response.json()
        access_token = data['access_token']
        profile_response = requests.get(
            f"{os.getenv('BASE_URL')}/profile",
            headers={'Authorization': f"Bearer {access_token}"},
            timeout=10
        )
        uid = profile_response.json()['uid']

        # Возвращаем успешный результат

        yield {
            'success': True,
            'access_token': access_token
        }

        # Удаление после теста
        requests.delete(
            f"{BASE_URL}/profile/total/{uid}",
            headers={'Authorization': f"Bearer {access_token}"},
            timeout=5
        )

    except Exception as e:
        # ловим ошибки
        yield {'success': False, 'error': str(e)}
