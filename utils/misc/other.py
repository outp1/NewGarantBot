import random
import glob
import os

from loader import deal_con

def rand_id_to_acc():
    def generate():
        rand_id = ''
        for x in range(8):
            rand_id = rand_id + ''.join([random.choice(list('1234567890'))])
        global _id
        _id = rand_id
        if deal_con.ids_to_exists(_id) == None:
            return _id
        else:
            return None
    while generate() == None:
        generate()
    return _id

def take_last_logfile():
    list_f = glob.glob('./logs/*')
    last_f = min(list_f, key=os.path.getctime)
    return last_f

