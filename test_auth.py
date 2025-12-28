import os
import requests
from pytest_check import check
import config

def test_signup_and_check(new_user_with_delete):
    """
    Тест регистрации и проверки данных
    """
    # 1. Данные от фикстуры (что сохранилось)
    user = new_user_with_delete

    # 2. Оригинальные данные из config (что должно было отправиться)
    original_config_data = config.body_new_user.copy()

    # 3. Получаем профиль
    BASE_URL = os.getenv("BASE_URL")
    headers = {'Authorization': f"Bearer {user['access_token']}"}
    profile_response = requests.get(
        f'{BASE_URL}/profile',
        headers=headers)
    profile_data = profile_response.json()

    # 4. Проверяем данные профиля
    with check.check():
        assert profile_data['first_name'] == original_config_data['first_name']
        assert profile_data['email'] == original_config_data['email']
        assert profile_data['phone_number'] == original_config_data['phone_number']
        assert profile_data['organization'] == original_config_data['organization']
        assert profile_data['timezone'] == original_config_data['timezone']
        assert profile_data['lang'] == original_config_data['lang']
        assert profile_data['rate'] == original_config_data['rate']

    print(f"Все проверки пройдены для пользователя {profile_data['email']}")


def test_user_delete_and_verify(new_user_with_delete):
    """
    Тест на удаление пользователя (код 200 при удалении) и проверку, что такого пользователя больше не существует
    """
    user = new_user_with_delete
    BASE_URL = os.getenv("BASE_URL")
    headers = {'Authorization': f"Bearer {user['access_token']}"}

    # 1. Удаляем пользователя
    delete_response = requests.delete(
        f'{BASE_URL}/profile/total/{user["uid"]}',
        headers=headers
    )

    #2. Проверяем успешное удаление
    with check.check():
        assert delete_response.status_code in [200, 204], \
            f"Удаление не удалось: {delete_response.status_code}"

    # 3. Проверяем что профиль недоступен
    profile_response = requests.get(f'{BASE_URL}/profile', headers=headers)

    with check.check():
        assert profile_response.status_code in [401, 403, 404], \
            f"Профиль все еще доступен: {profile_response.status_code}"

    print("Профиль недоступен")