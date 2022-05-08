from .sqlighter import Sqlighter

class ReferalsDatabase(Sqlighter):

    def __init__(self, db_name):
        self.db_name = db_name
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                table = '''
                        CREATE TABLE IF NOT EXISTS referals (
    link TEXT,
    refs INT    DEFAULT (0) 
);

                '''
                cursor.execute(table)
                connection.commit()

    def generate_link(self, text):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('INSERT INTO referals (link, refs) VALUES (%s, 0) ', (text,))
                connection.commit()

    def take_link(self, text):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('SELECT refs FROM referals WHERE link = %s', (text,))
                a = cursor.fetchone()[0]
                return a

    def update_ref(self, text):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('SELECT refs FROM referals WHERE link = %s', (text,))
                a = cursor.fetchone()[0]
                a = a + 1
                cursor.execute('UPDATE referals SET refs = %s WHERE link = %s', (a, text))
                connection.commit()

