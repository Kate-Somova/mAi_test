import json
import os
import allure
import psycopg2
import psycopg2.extras
import pytest
import pytest_check as check
from dotenv import load_dotenv
from data_test import russian_name_airport

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
def db_conn(scope="module"):
    conn = psycopg2.connect(
        host=os.getenv("HOST_DB"),
        port=os.getenv("PORT_DB"),
        database=os.getenv("DATABASE"),
        user=os.getenv("LOGIN_DB"),
        password=os.getenv("PASSWORD_DB")
    )
    conn.autocommit = False
    yield conn
    conn.close()


@pytest.fixture
def db_cursor(db_conn):
    cursor = db_conn.cursor()
    yield cursor
    db_conn.rollback()
    cursor.close()


@allure.feature('Базы данных')
@allure.story('Вытаскиваем из таблицы tickets одну строку по ticket_no')
def test_get_ticket_by_id(db_connection):
    with allure.step('Выполняю запрос'):
        db_connection.execute("SELECT * FROM airports_data WHERE ticket_no = %s", ('0005432000000',))

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
        # Название авиакомпании (вытащить)

    with allure.step('Выводим список'):
        print("\n2. Список:")
        print(list(ticket_tuple))
        # вытащить буллевое

    with allure.step('Выводим словарь'):
        columns = [desc[0] for desc in db_connection.description]
        print("\n3. Словарь:")
        print(dict(zip(columns, ticket_tuple)))
        # вытащить пассажир_id, чтобы ответ был в несколько строк

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
        # создать новую строку

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
        with check.check():
            assert row[1] == new_ticket['book_ref']
            assert row[2] == new_ticket['passenger_id']
            assert row[3] == new_ticket['passenger_name']
            assert row[4] == new_ticket['outbound']


@allure.feature('Базы данных')
@allure.story('Создание новой строки в таблице airports_data')
def test_create_airports(db_cursor):
    with allure.step('Формируем данные для нового аэропорта'):
        airport_code = '111'
        expected_name = {'en': 'Test Airport', 'ru': 'Тестовый аэропорт'}
        expected_city = {'en': 'Test City', 'ru': 'Тестовый город'}
        expected_country = {'en': 'Testland', 'ru': 'Тестландия'}
        expected_timezone = 'Europe/Moscow'

        new_airport = {
            'airport_code': airport_code,
            'airport_name': json.dumps(expected_name),
            'city': json.dumps(expected_city),
            'country': json.dumps(expected_country),
            'coordinates': '(12.34, 56.78)',
            'timezone': expected_timezone
        }

    with allure.step('Добавляем новую строку'):
        db_cursor.execute("""
            INSERT INTO airports_data
                (airport_code, airport_name, city, country, coordinates, timezone)
            VALUES
                (%(airport_code)s, %(airport_name)s, %(city)s, %(country)s, %(coordinates)s, %(timezone)s)
            """, new_airport)

    with allure.step('Проверяем, что строка создалась'):
        db_cursor.execute("SELECT * FROM airports_data WHERE airport_code = %s", (airport_code,))
        row = db_cursor.fetchone()
        with check.check():
            assert row[0] == airport_code
            assert row[1] == expected_name
            assert row[2] == expected_city
            assert row[3] == expected_country
            assert str(row[4]).replace(' ', '') == new_airport['coordinates'].replace(' ', '')
            assert row[5] == expected_timezone


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

        with check.check():
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


@allure.feature('Базы данных')
@allure.story('Получение flight_id из таблицы segments (переводим строку в число)')
def test_get_flight_id(db_cursor):
    with allure.step('Выполняем запрос для ticket_no = 0005432000014'):
        db_cursor.execute(
            "SELECT flight_id FROM segments WHERE ticket_no = %s",
            ('108',)
        )
        result = db_cursor.fetchone()

    with allure.step('Извлекаем flight_id и преобразуем в число'):
        flight_id = result[0]
        flight_id_int = int(flight_id)

    with allure.step('Проверяем и выводим результат'):
        assert flight_id_int == 970
        print(f"flight_id = {flight_id_int}")


@allure.feature('Базы данных')
@allure.story('Вытаскиваем из таблицы tickets несколько строк и проверяем их')
def test_select_tickets(db_cursor):
    with allure.step('Выполняем запрос'):
        db_cursor.execute(
            "SELECT * FROM tickets WHERE book_ref = %s",
            ('RBUUIQ',)
        )
        rows = db_cursor.fetchall()

    with allure.step('Выводим полученные строки'):
        print("Исходные строки:", rows)

    with allure.step('Проверка количества строк'):
        assert len(rows) == 4

    with allure.step('Проверка уникальных ticket_no (первый столбец)'):
        ticket_nos = {row[0] for row in rows}
        assert len(ticket_nos) == 4

    with allure.step('Проверка наличия определённых passenger_id (третий столбец)'):
        passenger_ids = {row[2] for row in rows}
        expected_ids = {'IT 2425980678984', 'IT 8025360863298'}
        assert passenger_ids == expected_ids

    with allure.step('Проверка уникальных пассажиров (четвёртый столбец)'):
        passenger_names = {row[3] for row in rows}
        assert len(passenger_names) == 2

    # with allure.step('Обновляем фамилию Cazzaniga на Cazza и outbound на True'):
    #     db_cursor.execute("""
    #         UPDATE tickets
    #         SET passenger_name = REPLACE(passenger_name, 'Cazzaniga', 'Cazza')
    #         WHERE book_ref = %s
    #     """, ('RBUUIQ',))
    #
    # with allure.step('Добавляем новую строку'):
    #     db_cursor.execute("""
    #         INSERT INTO tickets (ticket_no, book_ref, passenger_id, passenger_name, outbound)
    #         VALUES (%s, %s, %s, %s, %s)
    #     """, ('123456789', 'RBUUIQ', 'tst 101', 'Cruella De Vill', True))
    #
    #  with allure.step('Удаляем строку с ticket_no = 0005432000011 и outbound = True'):
    #      db_cursor.execute(
    #         "DELETE FROM tickets WHERE ticket_no = %s AND outbound = %s",
    #          ('0005432000011', True)
    #      )
    #
    # with allure.step('Повторно запрашиваем обновлённые строки'):
    #     db_cursor.execute(
    #         "SELECT * FROM tickets WHERE book_ref = %s",
    #         ('RBUUIQ',)
    #     )
    #     updated_rows = db_cursor.fetchall()
    #
    # with allure.step('Выводим изменённые строки'):
    #     print("Изменённые строки:", updated_rows)


def get_airport_code_by_russian_name(cursor, russian_name):
    cursor.execute("""
            SELECT airport_code
            FROM airports_data
            WHERE airport_name->>'ru' = %s
        """, (russian_name,))
    result = cursor.fetchone()
    return result[0] if result else None


@allure.feature('Базы данных')
@allure.story('Получение кодов нескольких аэропортов по русским названиям')
@pytest.mark.parametrize('russian_name', russian_name_airport)
def test_get_airport_codes(db_cursor, russian_name):
    with allure.step(f'Получаем код для "{russian_name}"'):
        code = get_airport_code_by_russian_name(db_cursor, russian_name)

    with allure.step('Вывод полученного кода'):
        print(f"{russian_name} - {code}")
