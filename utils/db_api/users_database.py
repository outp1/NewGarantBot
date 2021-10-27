from .sqlighter import Sqlighter
import datetime


class UsersDatabase(Sqlighter):

    def __init__(self, db_name):
        self.db_name = db_name

    #ПОЛУЧАЕМ ЮЗЕРА
    def user(self, _id, mention=None):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                user = cursor.execute('SELECT * FROM users WHERE user_id = ?', (_id,)).fetchone()
                if user:
                    if user[6] == 0 and mention:
                        user = cursor.execute('UPDATE users SET nickname = ? WHERE user_id = ?', (mention, _id)).fetchone()
                        return user
                    return user
                else:
                    reg_time = datetime.datetime.today().strftime("%d.%m.%Y")
                    user = cursor.execute('INSERT INTO users (user_id, registration_date) VALUES(?, ?)', (_id, reg_time))
                    connection.commit()
                    if mention:
                        user = cursor.execute('UPDATE users SET nickname = ? WHERE user_id = ?', (mention, _id))
                        connection.commit()
                    return user


    #ПОЛУЧАЕМ ПРОДАВЦА
    def seller(self, mention):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                seller = cursor.execute('SELECT * FROM users WHERE nickname = ?', (mention,)).fetchone()
                return seller




    """    def add_user(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                pass
"""
