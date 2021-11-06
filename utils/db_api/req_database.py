from .sqlighter import Sqlighter

class ReqDatabase(Sqlighter):

    def __init__(self, db_name):
        self.db_name = db_name

    def banker(self):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                return cursor.execute('SELECT * FROM req WHERE service = "banker"').fetchone()

    def switch_banker(self, token, api_hash, login, _pass):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('UPDATE req SET token = ?, api_hash = ?, login= ?, pass = ? WHERE service = "banker"', (token, api_hash, login, _pass))
                connection.commit()

    def qiwi(self):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                return cursor.execute('SELECT * FROM req WHERE service = "qiwi"').fetchone()

    def update_qiwi(self, token, login, _pass):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('UPDATE req SET token = ?, login = ?, pass = ? WHERE service = "qiwi"', (token, login, _pass))
                connection.commit()






"""
    
     def add_user(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                pass
                """