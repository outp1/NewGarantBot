from .sqlighter import Sqlighter

from .sqlighter import Sqlighter

class WithdrawDatabase(Sqlighter):

    def __init__(self, db_name):
        self.db_name = db_name

    # ДОБАВИТЬ ЗАЯВКУ
    def add_withdraw(self, _id, user_id, amount, method, req):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('INSERT INTO withdraw (uniq_id, user_id, amount, method, req) VALUES (?, ?, ?, ?, ?)', (_id, user_id, amount, method, req))
                connection.commit()
                a = cursor.execute('SELECT * FROM withdraw WHERE uniq_id = ?', (_id,)).fetchone()
                return a

    def update_withdraw(self, _id, status):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('UPDATE withdraw SET status = ? WHERE uniq_id = ?', (status, _id))
                connection.commit()

    def take_withdraw(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                return cursor.execute('SELECT * FROM withdraw WHERE uniq_id = ?', (_id,)).fetchone()




"""    def add_user(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                pass
"""