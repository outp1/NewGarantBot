import datetime

from .sqlighter import Sqlighter


class DealsDatabase(Sqlighter):

    def __init__(self, db_name):
        self.db_name = db_name
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                table = '''
                CREATE TABLE IF NOT EXISTS deals (
    deal_id     INT      NOT NULL,
    price       INT      NOT NULL,
    description TEXT      NOT NULL,
    client      INT      NOT NULL,
    seller      INT      NOT NULL,
    status      INTEGER  DEFAULT (0) 
                         NOT NULL,
    date        TIMESTAMP NOT NULL
);
'''
                cursor.execute(table)
                connection.commit()


    # ПРОВЕРЯЕМ АЙДИ НА НАЛИЧИЕ
    def ids_to_exists(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('SELECT deal_id FROM deals WHERE deal_id = %s', (_id,))
                result = cursor.fetchone()
                return result

    # СОЗДАЕМ НОВУЮ НЕПРИНЯТУЮ СДЕЛКУ
    def set_deal(self, deal_id, price, description, client, seller):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                date = datetime.datetime.today().strftime("%d.%m.%Y")
                cursor.execute(
                    'INSERT INTO deals (deal_id, price, description, client, seller, date) VALUES (%s, %s, %s, %s, %s, %s)',
                    (deal_id, price, description, client, seller, date))
                connection.commit()
                cursor.execute(
                    'SELECT * FROM deals WHERE deal_id = %s',
                    (int(deal_id),))
                deal = cursor.fetchone()
                return deal

    # ПОЛУЧАЕМ СДЕЛКУ ПО АЙДИ СДЕЛКИ
    def take_deal(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('SELECT * FROM deals WHERE deal_Id = %s', (_id,))
                deal = cursor.fetchone()
                return deal

    # ОБНОВЛЯЕМ СТАТУС СДЕЛКИ ЛИБО ВОЗВРАЩАЕМ ЗНАЧЕНИЕ
    def status(self, _id, status=None):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                if status:
                    cursor.execute('UPDATE deals SET status = %s WHERE deal_id = %s', (status, _id))
                    connection.commit()
                else:
                    cursor.execute('SELECT status FROM deals WHERE deal_id = %s', (_id))
                    return cursor.fetchone()

    def delete_deal(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('DELETE FROM deals WHERE deal_id = %s', (_id,))
                connection.commit()


    # АКТИВНЫЕ СДЕЛКИ ЮЗЕРА
    def active_deals(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('SELECT * FROM deals WHERE (seller = %s AND status = 0)', (_id,))
                un_sell_deals = cursor.fetchall()
                cursor.execute('SELECT * FROM deals WHERE (client = %s AND status = 0)', (_id,))
                un_buy_deals = cursor.fetchall()
                cursor.execute('SELECT * FROM deals WHERE (seller = %s AND status = 1)', (_id,))
                sell_deals = cursor.fetchall()
                cursor.execute('SELECT * FROM deals WHERE (client = %s AND status = 1)', (_id,))
                buy_deals = cursor.fetchall()
                return un_sell_deals, un_buy_deals, buy_deals, sell_deals




"""    def add_user(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                pass
"""
