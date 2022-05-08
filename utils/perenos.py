import psycopg2
from psycopg2 import Error

try:
    # Подключиться к существующей базе данных
    connection = psycopg2.connect(user="nmwyuhhthhuoop",
                                  # пароль, который указали при установке PostgreSQL
                                  password="37a16640ddcf56d50b1d0e2080822dac996eb06ab50d7e46bc7aa28910e847a7",
                                  host="ec2-52-3-130-181.compute-1.amazonaws.com",
                                  port="5432",
                                  database="d69n0e596186q1")

    cursor = connection.cursor()
    # Выполнение SQL-запроса для вставки данных в таблицу
    insert_query = """ CREATE TABLE IF NOT EXISTS users (
    user_id           INT    NOT NULL,
    registration_date DATE   NOT NULL,
    rating            CHAR   DEFAULT (0) 
                             NOT NULL,
    status            TEXT DEFAULT 'Неверифицрованный',
    earned            INT    DEFAULT (0) 
                             NOT NULL,
    balance           INT    DEFAULT (0) 
                             NOT NULL,
    nickname          TEXT DEFAULT (0),
    refs              INT    DEFAULT (0) 
) """

    cursor.execute(insert_query)
    connection.commit()

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")