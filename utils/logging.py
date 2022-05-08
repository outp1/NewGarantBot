import os
import logging
import json
import logging.config
from data import config


def create_logs_folder(folder=config.FOLDER_LOGS):
    if not os.path.exists(folder):
        os.mkdir(folder)

def get_logger(name, template='default'):
    create_logs_folder()
    with open(config.LOGGING_CONFIG_FILE, "r") as f:
        dict_config = json.load(f)
        dict_config["handlers"]["telegram"]["bot_token"] = config.BOT_TOKEN
        dict_config["handlers"]["telegram"]["admin_id"] = config.ADMIN
        dict_config["handlers"]["telegram"]["bot_name"] = config.BOT_NAME
        dict_config["loggers"][name] = dict_config["loggers"][template]
    logging.config.dictConfig(dict_config)
    return logging.getLogger(name)

def get_default_logger():
    create_logs_folder()
    with open(config.LOGGING_CONFIG_FILE, "r") as f:
        logging.config.dictConfig(json.load(f))
    return logging.getLogger("default")

