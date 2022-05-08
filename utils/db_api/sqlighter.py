import psycopg2
from data import config

class Sqlighter:

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.connection = psycopg2.connect(user=config.POSTGRESQLITE['user'],
                                  # пароль, который указали при установке PostgreSQL
                                  password=config.POSTGRESQLITE['password'],
                                  host=config.POSTGRESQLITE['host'],
                                  port=config.POSTGRESQLITE['port'],
                                  database=config.POSTGRESQLITE['database'])
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        if exc_val:
            raise




