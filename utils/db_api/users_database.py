from .sqlighter import Sqlighter
import datetime


class UsersDatabase(Sqlighter):

    def __init__(self, db_name):
        self.db_name = db_name

    #ПОЛУЧАЕМ ЮЗЕРА
    def user(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                user = cursor.execute('SELECT * FROM users WHERE user_id = ?', (_id,)).fetchone()
                if user:
                    return user
                else:
                    reg_time = datetime.datetime.today().strftime("%d.%m.%Y")
                    user = cursor.execute('INSERT INTO users (user_id, registration_date) VALUES(?, ?)', (_id, reg_time))
                    connection.commit()
                    return user

    #ПОЛУЧАЕМ ПРОДАВЦА
    def seller(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                seller = cursor.execute('SELECT * FROM users WHERE user_id = ?', (_id,)).fetchone()
                return seller

    """    def add_user(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                pass
"""
