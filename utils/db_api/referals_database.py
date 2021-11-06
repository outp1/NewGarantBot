from .sqlighter import Sqlighter

class ReferalsDatabase(Sqlighter):

    def __init__(self, db_name):
        self.db_name = db_name

    def generate_link(self, text):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('INSERT INTO referals (link, refs) VALUES (?, 0) ', (text,))
                connection.commit()

    def take_link(self, text):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                a = cursor.execute('SELECT refs FROM referals WHERE link = ?', (text,)).fetchone()[0]
                return a

    def update_ref(self, text):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                a = cursor.execute('SELECT refs FROM referals WHERE link = ?', (text,)).fetchone()[0]
                a = a + 1
                cursor.execute('UPDATE referals SET refs = ? WHERE link = ?', (a, text))
                connection.commit()

