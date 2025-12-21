import pytest
import requests

@pytest.fixture
def body_new_user():
    return {
    "email": "test6@example.com",
    "password": "string",
    "first_name": "Kate",
    "last_name": "Somova",
    "timezone": "+3",
    "organization": "OON",
    "phone_number": "+7(926)777-77-79",
    "phone_country_code": "+7",
    "lang": "RU",
    "rate": "org"
}


@pytest.fixture
def create_new_user(body_new_user):
# Создание пользователя
    response = requests.post(
        'https://mai-tech.ru/api/auth/signup/',
        json=body_new_user
    )

    # Если создание не удалось, падает ошибка
    assert response.status_code == 200, f"Ошибка создания пользователя: {response.status_code}"

    # Получаем токен
    data = response.json()
    access_token = data['access_token']

    # Получаем UID пользователя
    profile_response = requests.get(
        'https://mai-tech.ru/api/profile',
        headers={'Authorization': f"Bearer {access_token}"}
    )

    assert profile_response.status_code == 200, f"Ошибка получения профиля: {profile_response.status_code}"

    uid = profile_response.json()['uid']

    # Возвращаем данные для теста (без автоматического удаления!)
    return {
        "access_token": access_token,
        "uid": uid,
        "user_data": body_new_user,
        "response_data": data  # полный ответ от сервера
    }


@pytest.fixture
def cleanup_user():
    """Фикстура для удаления пользователя после теста"""
    users_to_delete = []

    def _register_for_cleanup(uid, token):
        users_to_delete.append((uid, token))

    yield _register_for_cleanup

    # После теста удаляем всех зарегистрированных пользователей
    for uid, token in users_to_delete:
        requests.delete(
            f'https://mai-tech.ru/api/profile/total/{uid}',
            headers={'Authorization': f"Bearer {token}"},
            timeout=5
        )