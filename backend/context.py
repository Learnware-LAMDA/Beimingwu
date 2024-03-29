"""context.py: All globals should be defined here.

"""
import os
from config import Config
from database import Database, SQLAlchemy
from typing import List

from learnware.market import instantiate_learnware_market
from learnware.config import C as leanrware_conf
import logging
import redis
import re
import concurrent_log_handler


database: Database = None
engine = None
engine_config = None
redis_client = None
stats = 0
sensitive_pattern = None

config = Config()

logger = logging.getLogger("")


class MyConcurrentTimedRotatingFileHandler(concurrent_log_handler.ConcurrentTimedRotatingFileHandler):
    def getFilesToDelete(self) -> List[str]:
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        results = []
        for fileName in fileNames:
            if fileName.startswith(baseName):
                results.append(os.path.join(dirName, fileName))
                pass
            pass
        results.sort()

        if self.backupCount <= 0:
            return results
        else:
            return results[: -self.backupCount]
        pass


def init_database(admin_password: str = None):
    global config, database

    if config.database["type"] == "sqlalchemy":
        database = SQLAlchemy(config=config.database, admin_password=admin_password)
        pass

    if database is None:
        raise ValueError(f"Database type {config.database['type']} is not supproted.")
    pass


def init_engine():
    global config, engine, engine_config
    if config.engine["type"] == "easy":
        engine = instantiate_learnware_market(market_id="default", name="eazy", rebuild=False)
        engine_config = leanrware_conf
    elif config.engine["type"] == "hetero":
        engine = instantiate_learnware_market(
            market_id="default", name="hetero", rebuild=False, organizer_kwargs={"auto_update": False}
        )
        engine_config = leanrware_conf
    else:
        raise ValueError(f"Learnware engine type {config.engine['type']} is not supproted.")
    pass


def init_backend():
    global config

    os.makedirs(config.upload_path, exist_ok=True)
    os.makedirs(config.temp_path, exist_ok=True)
    os.makedirs(config.backup_path, exist_ok=True)
    os.makedirs(config.datasets_path, exist_ok=True)
    os.makedirs(config.log_path, exist_ok=True)
    os.makedirs(config.env_path, exist_ok=True)
    pass


def init_redis():
    global config, redis_client

    redis_client = redis.Redis(host=config.redis["host"], port=config.redis["port"], decode_responses=True)
    pass


def init_logger(target="console"):
    global config, logger

    if len(logger.handlers) > 0:
        pass
    elif target == "console":
        handler = logging.StreamHandler()
    elif target == "file":
        log_path = config["log_path"]
        hostname = os.environ.get("HOSTNAME")
        if hostname is None:
            hostname = "learnware-backend"
            pass

        filename = os.path.join(log_path, f"{hostname}.log")
        handler = MyConcurrentTimedRotatingFileHandler(
            filename=filename, when="d", interval=1, backupCount=180, encoding="utf-8"
        )
        pass

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    logger.setLevel(logging.DEBUG)

    pass


def init_sensitive_words():
    global sensitive_pattern
    word_file = config["sensitive_word_file"]
    sensitive_words = []
    if os.path.exists(word_file):
        with open(word_file) as fin:
            for line in fin:
                w = line.strip()
                if len(w) > 0:
                    if w.isascii():
                        w = " " + w + " "
                        pass

                    sensitive_words.append(re.escape(w))
                    pass
                pass
            pass
        sensitive_pattern = re.compile("(" + "|".join(sensitive_words) + ")")
        pass
    pass


def get_learnware_verify_file_path(learnware_id):
    return os.path.join(config.upload_path, f"{learnware_id}.zip")
