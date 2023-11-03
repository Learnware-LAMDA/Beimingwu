"""context.py: All globals should be defined here.

"""
import os
from config import Config
from database import Database, SQLAlchemy

from learnware.market import EasyMarket
from market.backend_market import BackendMarket
import logging


database: Database = None
engine = None
stats = 0

config = Config()

logger = logging.getLogger("learnware-backend")


def init_database(admin_password: str = None):
    global config, database

    if config.database["type"] == "sqlalchemy":
        database = SQLAlchemy(config=config.database, admin_password=admin_password)
        pass

    if database is None:
        raise ValueError(f"Database type {config.database['type']} is not supproted.")
    pass


def init_engine():
    global config, engine
    if config.engine["type"] == "easymarket":
        engine = EasyMarket()
    elif config.engine["type"] == "backend_market":
        engine = BackendMarket()
    else:
        raise ValueError(f"Learnware engine type {config.engine_type} is not supproted.")
    pass


def init_backend():
    global config

    os.makedirs(config.upload_path, exist_ok=True)
    os.makedirs(config.temp_path, exist_ok=True)
    os.makedirs(config.backup_path, exist_ok=True)
    pass


def init_logger():
    global config, logger

    if len(logger.handlers) > 0:
        pass
    else:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        pass

    logger.setLevel(logging.DEBUG)

    pass


def get_learnware_verify_file_path(learnware_id):
    return os.path.join(config.upload_path, f"{learnware_id}.zip")
