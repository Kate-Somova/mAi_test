import os

import allure
import psycopg2
import pytest
import pytest_check
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture()
def db_connection():
    with allure.step("Подключение к базе данных"):
        conn = psycopg2.connect(
            host=os.getenv("HOST_DB"),
            port=os.getenv("PORT_DB"),
            database=os.getenv("DATABASE"),
            user=os.getenv("LOGIN_DB"),
            password=os.getenv("PASSWORD_DB")
        )
        cursor = conn.cursor()
    yield cursor
    with allure.step("Закрытие соединения с БД"):
        cursor.close()
        conn.close()

@pytest.fixture
def db_cursor():
    with allure.step("Подключение к БД с отключённым autocommit"):
        conn = psycopg2.connect(
            host=os.getenv("HOST_DB"),
            port=os.getenv("PORT_DB"),
            database=os.getenv("DATABASE"),
            user=os.getenv("LOGIN_DB"),
            password=os.getenv("PASSWORD_DB")
        )
        conn.autocommit = False
        cursor = conn.cursor()
    yield cursor
    with allure.step("Откат изменений и закрытие соединения"):
        conn.rollback()
        cursor.close()
        conn.close()

@allure.feature('Базы данных')
@allure.story('Вытаскиваем из таблицы tickets одну строку по ticket_no')
def test_get_ticket_by_id(db_connection):
    with allure.step('Выполняю запрос'):
        db_connection.execute("SELECT * FROM tickets WHERE ticket_no = %s", ('0005432000000',))

    with allure.step('Получаем одну строку'):
        ticket = db_connection.fetchone()

    with allure.step('Выводим полученные данные'):
        print(ticket)

@allure.feature('Базы данных')
@allure.story('Смотрим разные типы данных при выводе результата запроса бд')
def test_data_structures(db_connection):
    with allure.step('Выполняем запрос для получения одной записи'):
        db_connection.execute(
            "SELECT * FROM tickets WHERE ticket_no = %s",
            ('0005432000000',)
        )
        ticket_tuple = db_connection.fetchone()

    with allure.step('Выводим кортеж'):
        print("\n1. Кортеж (оригинал из БД):")
        print(ticket_tuple)

    with allure.step('Выводим список'):
        print("\n2. Список:")
        print(list(ticket_tuple))

    with allure.step('Выводим словарь'):
        columns = [desc[0] for desc in db_connection.description]
        print("\n3. Словарь:")
        print(dict(zip(columns, ticket_tuple)))

    with allure.step('Выводим множество'):
        print("\n4. Множество:")
        print(set(ticket_tuple))

@allure.feature('Базы данных')
@allure.story('Создание новой строки в таблице tickets')
def test_create_ticket(db_cursor):
    with allure.step('Получаем любой существующий book_ref из таблицы bookings'):
        db_cursor.execute("SELECT book_ref FROM bookings LIMIT 1")
        result = db_cursor.fetchone()
        existing_book_ref = result[0]

    with allure.step('Присваиваем значения для новой строки'):
        new_ticket = {
            'ticket_no': '101',
            'book_ref': existing_book_ref,
            'passenger_id': '101 TEST',
            'passenger_name': 'Cruella de Vil',
            'outbound': False
        }

    with allure.step('Добавляем новую строку'):
        db_cursor.execute("""
            INSERT INTO tickets (ticket_no, book_ref, passenger_id, passenger_name, outbound)
            VALUES (%(ticket_no)s, %(book_ref)s, %(passenger_id)s, %(passenger_name)s, %(outbound)s)
        """, new_ticket)

    with allure.step('Проверяем, что строка создалась'):
        db_cursor.execute("SELECT * FROM tickets WHERE ticket_no = %s", (new_ticket['ticket_no'],))
        row = db_cursor.fetchone()
        with pytest_check.check.check():
            assert row[1] == new_ticket['book_ref']
            assert row[2] == new_ticket['passenger_id']
            assert row[3] == new_ticket['passenger_name']
            assert row[4] == new_ticket['outbound']

@allure.feature('Базы данных')
@allure.story('Обновление строки в таблице tickets')
def test_update_ticket(db_cursor):
    with allure.step('Получаем существующий book_ref'):
        db_cursor.execute("SELECT book_ref FROM bookings LIMIT 1")
        existing_book_ref = db_cursor.fetchone()[0]

    with allure.step('Создаём тестовую строку, которую будем обновлять'):
        ticket_no = '102'
        db_cursor.execute("""
            INSERT INTO tickets (ticket_no, book_ref, passenger_id, passenger_name, outbound)
            VALUES (%s, %s, %s, %s, %s)
        """, (ticket_no, existing_book_ref, '102 TEST', 'Cruella de Vil', False))

    with allure.step('Обновляем поле passenger_name'):
        new_name = 'Estelle De Vil'
        db_cursor.execute("""
            UPDATE tickets
            SET passenger_name = %s
            WHERE ticket_no = %s
        """, (new_name, ticket_no))

    with allure.step('Проверяем, что обновление прошло успешно'):
        db_cursor.execute("SELECT * FROM tickets WHERE ticket_no = %s", (ticket_no,))
        row = db_cursor.fetchone()
        assert row is not None, "Запись не найдена после обновления"

        with pytest_check.check.check():
            assert row[3] == new_name, "passenger_name не обновилось"
            # Проверяем, что остальные поля не изменились (кроме обновлённых)
            assert row[1] == existing_book_ref, "book_ref изменился"
            assert row[2] == '102 TEST', "passenger_id изменился"
            assert row[4] == False, "outbound не изменился"

@allure.feature('Базы данных')
@allure.story('Удаление строки в таблице tickets')
def test_delete_ticket(db_cursor):
    with allure.step('Получаем существующий book_ref'):
        db_cursor.execute("SELECT book_ref FROM bookings LIMIT 1")
        existing_book_ref = db_cursor.fetchone()[0]

    with allure.step('Создаём новую строку, которую будем удалять'):
        ticket_no = '103'
        db_cursor.execute("""
            INSERT INTO tickets (ticket_no, book_ref, passenger_id, passenger_name, outbound)
            VALUES (%s, %s, %s, %s, %s)
        """, (ticket_no, existing_book_ref, '103 TEST', 'Cruella de Vil', False))

    with allure.step('Проверяем, что запись действительно появилась'):
        db_cursor.execute("SELECT * FROM tickets WHERE ticket_no = %s", (ticket_no,))
        row_before = db_cursor.fetchone()
        assert row_before is not None, "Запись не создалась перед удалением"

    with allure.step('Удаляем запись'):
        db_cursor.execute("DELETE FROM tickets WHERE ticket_no = %s", (ticket_no,))

    with allure.step('Проверяем, что записи больше нет'):
        db_cursor.execute("SELECT * FROM tickets WHERE ticket_no = %s", (ticket_no,))
        row_after = db_cursor.fetchone()
        assert row_after is None, "Запись не была удалена"