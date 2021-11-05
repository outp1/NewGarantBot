from .sqlighter import Sqlighter

class FeedDatabase(Sqlighter):

    def __init__(self, db_name):
        self.db_name = db_name

    # Добавляем отзыва
    def add_feed(self, deal, seller, rate):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('INSERT INTO feed (deal, seller, rate) VALUES (?, ?, ?)', (deal, seller, rate))
                connection.commit()

    # Обновляем отзыв
    def update_feed(self, deal, feedback):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute("UPDATE feed SET feedback = ? WHERE deal = ?", (feedback, deal))
                connection.commit()
                return cursor.execute("SELECT * FROM feed WHERE deal = ?").fetchone()

    # Получаем все отзывы
    def get_feeds(self, seller):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                return cursor.execute("SELECT * FROM feed WHERE seller = ?", (seller,)).fetchall()

    # Считаем рейтинг
    def calc_rating(self, seller):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                sum1 = cursor.execute("SELECT rate FROM feed WHERE seller = ?", (seller,)).fetchall()
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

