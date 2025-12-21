import requests
from pytest_check import check

import config


def test_signup_200(body_new_user, cleanup_user):
    # Регистрация
    response = requests.post(
        'https://mai-tech.ru/api/auth/signup/',
        json=body_new_user
    )
    assert response.status_code == 200

    # Получаем данные
    data = response.json()
    access_token = data['access_token']

    response = requests.get(
        'https://mai-tech.ru/api/profile',
        headers={'Authorization': f"Bearer {access_token}"}
    )
    uid = response.json()['uid']

    # Регистрируем для очистки
    cleanup_user(uid, access_token)
#Система не удаляет пользователя

def test_signup_and_check(body_new_user, cleanup_user):
    """Тест регистрации и проверки данных"""
    # 1. Регистрация
    response = requests.post(
        'https://mai-tech.ru/api/auth/signup/',
        json=body_new_user
    )
    assert response.status_code == 200

    # 2. Получаем токен и данные
    data = response.json()
    access_token = data['access_token']

    # 3. Получаем профиль
    headers = {'Authorization': f"Bearer {access_token}"}
    profile_response = requests.get('https://mai-tech.ru/api/profile', headers=headers)
    profile_data = profile_response.json()
    uid = profile_data['uid']

    # 4. Проверяем данные профиля
    with check.check():
        # Проверяем что данные в профиле совпадают с отправленными
        assert profile_data['first_name'] == body_new_user['first_name']
        assert profile_data['email'] == body_new_user['email']
        assert profile_data['phone_number'] == body_new_user['phone_number']
        assert profile_data['organization'] == body_new_user['organization']
        assert profile_data['timezone'] == body_new_user['timezone']
        assert profile_data['lang'] == body_new_user['lang']
        assert profile_data['rate'] == body_new_user['rate']

    print(f"Пользователь создан, UID: {uid}")

    # 5. Регистрируем для очистки
    cleanup_user(uid, access_token)


def test_user_delete_and_verify(create_new_user):
    """
    Тест на удаление пользователя (код 200 при удалении) и проверку, что такого пользователя больше не существует
    """
    access_token = create_new_user["access_token"]
    uid = create_new_user["uid"]

    headers = {'Authorization': f"Bearer {access_token}"}

    # 1. Удаляем пользователя
    delete_response = requests.delete(
        f'https://mai-tech.ru/api/profile/total/{uid}',
        headers=headers
    )

    # Проверяем успешное удаление (200)
    assert delete_response.status_code == 200, \
        f"Ошибка удаления: {delete_response.status_code}, текст: {delete_response.text}"

    # 2. Пробуем получить профиль удаленного пользователя
    # (должна быть 401 Unauthorized или 404 Not Found)
    get_response = requests.get(
        'https://mai-tech.ru/api/profile',
        headers=headers
    )
   # Проверяем что доступ к профилю закрыт
    assert get_response.status_code in [401, 403, 404], \
        f"Профиль все еще доступен: {get_response.status_code}"