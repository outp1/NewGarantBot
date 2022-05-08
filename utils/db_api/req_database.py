from .sqlighter import Sqlighter

class ReqDatabase(Sqlighter):

    def __init__(self, db_name):
        self.db_name = db_name
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                table = '''
                CREATE TABLE IF NOT EXISTS req (
    service  TEXT,
    token    TEXT,
    api_hash TEXT,
    login   VARCHAR(50),
    pass     TEXT
);
                        '''
                cursor.execute(table)
                connection.commit()

    def banker(self):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute("SELECT * FROM req WHERE service = 'banker'")
                return cursor.fetchone()

    def switch_banker(self, token, api_hash, login, _pass):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute("UPDATE req SET token = %s, api_hash = %s, login= %s, pass = %s WHERE service = 'banker'", (token, api_hash, login, _pass))
                connection.commit()

    def qiwi(self):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute("SELECT * FROM public.req WHERE service = 'qiwi'")
                return cursor.fetchone()

    def update_qiwi(self, token, login, _pass):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute("UPDATE req SET token = %s, login = %s, pass = %s WHERE service = 'qiwi'", (token, login, _pass))
                connection.commit()






"""
    
     def add_user(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                pass
                """