import os
import requests
import pytest_check
import config

def test_signup_and_check(new_user_with_delete):
    """
    Тест регистрации и проверки данных
    """
    # 1. Вытаскиваем данные из config
    body_new_user = config.body_new_user.copy()

    # 2. Получаем профиль
    BASE_URL = os.getenv("BASE_URL")
    headers = {'Authorization': f"Bearer {new_user_with_delete['access_token']}"}
    profile_response = requests.get(
        f'{BASE_URL}/profile',
        headers=headers)
    profile_body = profile_response.json()

    # 3. Сама проверка данных профиля
    with pytest_check.check.check():
        assert profile_body['first_name'] == body_new_user['first_name']
        assert profile_body['email'] == body_new_user['email']
        assert profile_body['phone_number'] == body_new_user['phone_number']
        assert profile_body['organization'] == body_new_user['organization']
        assert profile_body['timezone'] == body_new_user['timezone']
        assert profile_body['lang'] == body_new_user['lang']
        assert profile_body['rate'] == body_new_user['rate']

    print(f"Все проверки пройдены для пользователя {profile_body['email']}")


def test_user_delete_and_verify(new_user_with_delete):
    """
    Тест на удаление пользователя (код 200 при удалении) и проверку, что такого пользователя больше не существует
    """
    new_user = new_user_with_delete
    BASE_URL = os.getenv("BASE_URL")
    headers = {'Authorization': f"Bearer {new_user['access_token']}"}

    # 1. Удаляем пользователя
    delete_response = requests.delete(
        f'{BASE_URL}/profile/total/{new_user["uid"]}',
        headers=headers
    )

    #2. Проверяем успешное удаление
    with pytest_check.check.check():
        assert delete_response.status_code in [200, 204], \
            f"Удаление не удалось: {delete_response.status_code}"

    # 3. Проверяем что профиль недоступен
    profile_response = requests.get(f'{BASE_URL}/profile', headers=headers)

    with pytest_check.check.check():
        assert profile_response.status_code in [401, 403, 404], \
            f"Профиль все еще доступен: {profile_response.status_code}"

    print("Профиль недоступен")