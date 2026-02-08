import os
import pytest
import requests
import pytest_check
import config

def test_signup_and_check(new_user_with_delete):
    """
    Тест регистрации и проверки данных
    """
    # Проверяем результат фикстуры
    # Если фикстура выдала ошибку, то тест останавливается и печатается ошибка
    if not new_user_with_delete.get('success', False):
        error_msg = new_user_with_delete.get('error', 'Неизвестная ошибка создания пользователя')
        print(f"Ошибка: {error_msg}")
        pytest.fail(error_msg)
        return

    # Если успешно - продолжается работа теста (получаем данные профиля из бд)
    BASE_URL = os.getenv("BASE_URL")
    headers = {'Authorization': f"Bearer {new_user_with_delete['access_token']}"}
    profile_response = requests.get(
        f'{BASE_URL}/profile',
        headers=headers
    )
    profile_body = profile_response.json()
    # 3. Проверка данных профиля
    with pytest_check.check.check():
        assert profile_body['first_name'] == config.body_new_user['first_name']
        assert profile_body['email'] == config.body_new_user['email']
        assert profile_body['phone_number'] == config.body_new_user['phone_number']
        assert profile_body['organization'] == config.body_new_user['organization']
        assert profile_body['timezone'] == config.body_new_user['timezone']
        assert profile_body['lang'] == config.body_new_user['lang']
        assert profile_body['rate'] == config.body_new_user['rate']



def test_user_delete_and_verify():
    """
    Тест на удаление пользователя (код 200 при удалении) и проверку, что профиль не доступен
    """
    # Создание пользователя
    BASE_URL = os.getenv("BASE_URL")
    create_response = requests.post(
        f'{BASE_URL}/auth/signup/',
        json=config.body_new_user,
        timeout=10
    )

    # Если email занят - тест падает
    if create_response.status_code == 409:
        pytest.fail(f"Email '{config.body_new_user['email']}' уже занят")

    assert create_response.status_code == 200, f"Ошибка создания: {create_response.status_code}"

    # Получение токена и UID
    access_token = create_response.json()['access_token']
    profile_response = requests.get(
        f'{BASE_URL}/profile',
        headers={'Authorization': f"Bearer {access_token}"}
    )
    uid = profile_response.json()['uid']

    # Удаляем пользователя
    headers = {'Authorization': f"Bearer {access_token}"}
    delete_response = requests.delete(
        f'{BASE_URL}/profile/total/{uid}',
        headers=headers
    )

    # Проверяем успешное удаление
    with pytest_check.check.check():
        assert delete_response.status_code in [200, 204], \
            f"Удаление не удалось: {delete_response.status_code}"

    # Проверяем что профиль недоступен
    profile_response = requests.get(
        f'{BASE_URL}/profile',
        headers=headers,
        timeout=10
    )

    with pytest_check.check.check():
        assert profile_response.status_code in [401, 403, 404], \
            f"Профиль все еще доступен: {profile_response.status_code}"