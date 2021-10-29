import datetime

from .sqlighter import Sqlighter


class DealsDatabase(Sqlighter):

    def __init__(self, db_name):
        self.db_name = db_name

    # ПРОВЕРЯЕМ АЙДИ НА НАЛИЧИЕ
    def ids_to_exists(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                result = cursor.execute('SELECT deal_id FROM deals WHERE deal_id = ?', (_id,)).fetchone()
                return result

    # СОЗДАЕМ НОВУЮ НЕПРИНЯТУЮ СДЕЛКУ
    def set_deal(self, deal_id, price, description, client, seller):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                date = datetime.datetime.today().strftime("%d.%m.%Y")
                cursor.execute(
                    'INSERT INTO deals (deal_id, price, description, client, seller, date) VALUES (?, ?, ?, ?, ?, ?)',
                    (deal_id, price, description, client, seller, date))
                connection.commit()
                deal = cursor.execute(
                    'SELECT * FROM deals WHERE deal_id = ?',
                    (int(deal_id),)).fetchone()
                return deal

    # ПОЛУЧАЕМ СДЕЛКУ ПО АЙДИ СДЕЛКИ
    def take_deal(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                deal = cursor.execute('SELECT * FROM deals WHERE deal_Id = ?', (_id,)).fetchone()
                return deal

    # ОБНОВЛЯЕМ СТАТУС СДЕЛКИ ЛИБО ВОЗВРАЩАЕМ ЗНАЧЕНИЕ
    def status(self, _id, status=None):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                if status:
                    cursor.execute('UPDATE deals SET status = ? WHERE deal_id = ?', (status, _id))
                    connection.commit()
                else:
                    return cursor.execute('SELECT status FROM deals WHERE deal_id = ?', (_id)).fetchone()

    def delete_deal(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                cursor.execute('DELETE FROM deals WHERE deal_id = ?', (_id,))
                connection.commit()


    # АКТИВНЫЕ СДЕЛКИ ЮЗЕРА
    def active_deals(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                un_sell_deals = cursor.execute('SELECT * FROM deals WHERE seller = ? AND status = 0', (_id,)).fetchall()
                un_buy_deals = cursor.execute('SELECT * FROM deals WHERE client = ? AND status = 0', (_id,)).fetchall()
                sell_deals = cursor.execute('SELECT * FROM deals WHERE seller = ? AND status = 1', (_id,)).fetchall()
                buy_deals = cursor.execute('SELECT * FROM deals WHERE client = ? AND status = 1', (_id,)).fetchall()
                return un_sell_deals, un_buy_deals, buy_deals, sell_deals




"""    def add_user(self, _id):
        with Sqlighter(self.db_name) as connection:
            cursor = connection.cursor()
            with connection:
                pass
"""
