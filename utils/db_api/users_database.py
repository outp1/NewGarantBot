from .sqlighter import Sqlighter
import datetime


class UsersDatabase(Sqlighter):

    def __init__(self, db_name):
        self.db_name = db_name
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                table = """
                CREATE TABLE IF NOT EXISTS users (
    user_id           INT    NOT NULL,
    registration_date DATE   NOT NULL,
    rating            NUMERIC   DEFAULT (0) 
                             NOT NULL,
    status            TEXT DEFAULT 'Неверифицрованный',
    earned            INT    DEFAULT (0) 
                             NOT NULL,
    balance           INT    DEFAULT (0) 
                             NOT NULL,
    nickname          TEXT DEFAULT (0),
    refs              INT    DEFAULT (0) 
);

        """
                cursor.execute(table)
                connection.commit()

    #ПОЛУЧАЕМ ЮЗЕРА
    def user(self, _id, mention=None, ref=None):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('SELECT * FROM users WHERE user_id = %s', (_id,))
                user = cursor.fetchone()
                if user:
                    if user[6] == 0 and mention:
                        cursor.execute('UPDATE users SET nickname = %s WHERE user_id = %s', (mention, _id))
                    return user
                else:

                    reg_time = datetime.datetime.today().strftime("%Y-%m-%d")
                    cursor.execute('INSERT INTO users (user_id, registration_date) VALUES(%s, DATE %s)', (_id, reg_time))
                    connection.commit()
                    if mention:
                        cursor.execute('UPDATE users SET nickname = %s WHERE user_id = %s', (mention, _id))
                        connection.commit()
                    if ref:
                        self.add_ref(ref)


    #ПОЛУЧАЕМ ПРОДАВЦА
    def seller(self, mention):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('SELECT * FROM users WHERE nickname = %s', (mention,))
                seller = cursor.fetchone()
                return seller

    def update_balance(self, _id, amount2, earned_status=False, minus=True):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                if not minus:
                    cursor.execute('SELECT balance FROM users WHERE user_id = %s', (_id,))
                    amount1 = int(cursor.fetchone()[0])
                    balance = amount1 + int(amount2)
                if minus:
                    cursor.execute('SELECT balance FROM users WHERE user_id = %s', (_id,))
                    amount1 = int(cursor.fetchone()[0])
                    balance = amount1 - int(amount2)
                if earned_status:
                    cursor.execute('SELECT earned FROM users WHERE user_id= %s', (_id,))
                    earned1 = int(cursor.fetchone()[0])
                    earned = earned1 + amount2
                    cursor.execute('UPDATE users SET earned = %s WHERE user_id = %s', (earned, _id))
                    connection.commit()
                cursor.execute('UPDATE users SET balance = %s WHERE user_id = %s', (balance, _id))
                connection.commit()

    def update_rating(self, _id, rate):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                rate = float("{0:.1f}".format(rate))
                cursor.execute('UPDATE users SET rating = %s WHERE user_id = %s', (rate, _id))
                connection.commit()

    def take_verif(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute("UPDATE users SET status = 'Верифицированный' WHERE user_id = %s", (_id,))
                connection.commit()

    def add_ref(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                try:
                    cursor.execute('SELECT refs FROM users WHERE user_id = %s', (_id,))
                    amount = cursor.fetchone()[0]
                    amount = amount + 1
                    cursor.execute('UPDATE users SET refs = %s WHERE user_id = %s', (amount, _id))
                    connection.commit()
                except:
                    cursor.execute('SELECT refs FROM referals WHERE link = %s', (_id,))
                    a = cursor.fetchone()[0]
                    a = a + 1
                    cursor.execute('UPDATE referals SET refs = %s WHERE link = %s', (a, _id))
                    connection.commit()

    def check_refs(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('SELECT user_id, refs FROM users WHERE user_id = %s', (_id,))
                return cursor.fetchone()

    def set_balance(self, _id, amount):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('UPDATE users SET balance = %s WHERE user_id = %s', (amount, _id))
                connection.commit()




    """    def add_user(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                pass
"""
