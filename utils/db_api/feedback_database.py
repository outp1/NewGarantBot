from .sqlighter import Sqlighter

class FeedDatabase(Sqlighter):

    def __init__(self, db_name):
        self.db_name = db_name
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                table = '''
                CREATE TABLE IF NOT EXISTS feed (
    deal     INT    NOT NULL,
    seller   INT    NOT NULL,
    feedback TEXT,
    rate     INT
);
        '''
                cursor.execute(table)
                connection.commit()

    # Добавляем отзыва
    def add_feed(self, deal, seller, rate):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('INSERT INTO feed (deal, seller, rate) VALUES (%s, %s, %s)', (deal, seller, rate))
                connection.commit()

    # Обновляем отзыв
    def update_feed(self, deal, feedback):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute("UPDATE feed SET feedback = %s WHERE deal = %s", (feedback, deal))
                connection.commit()
                cursor.execute("SELECT * FROM feed WHERE deal = %s")
                return cursor.fetchone()

    # Получаем все отзывы
    def get_feeds(self, seller):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute("SELECT * FROM feed WHERE seller = %s", (seller,))
                return cursor.fetchall()

    # Считаем рейтинг
    def calc_rating(self, seller):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                sum1 = cursor.execute("SELECT rate FROM feed WHERE seller = %s", (seller,))
                sum1 = cursor.fetchall()
                sum = 0
                i = 0
                for a in sum1:
                    i = i + 1
                    sum = sum + int(a[0])
                sum = sum / i
                return sum









"""    def add_user(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                pass
"""

