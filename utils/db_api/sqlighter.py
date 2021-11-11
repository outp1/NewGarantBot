import psycopg2

#Config
POSTGRESQLITE = {
    'user': 'nmwyuhhthhuoop',
    'password': '37a16640ddcf56d50b1d0e2080822dac996eb06ab50d7e46bc7aa28910e847a7',
    'host': 'ec2-52-3-130-181.compute-1.amazonaws.com',
    'port': '5432',
    'database': 'd69n0e596186q1'}

class Sqlighter:

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.connection = psycopg2.connect(user=POSTGRESQLITE['user'],
                                  # пароль, который указали при установке PostgreSQL
                                  password=POSTGRESQLITE['password'],
                                  host=POSTGRESQLITE['host'],
                                  port=POSTGRESQLITE['port'],
                                  database=POSTGRESQLITE['database'])
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        if exc_val:
            raise


