import os
import copy
import json


class Config:
    def __init__(self, default_conf=None):
        if default_conf is None:
            default_conf = _DEFAULT_CONFIG
            pass

        self.__dict__["_default_config"] = copy.deepcopy(default_conf)  # avoiding conflictions with __getattr__
        self.reset()

        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                self.__dict__["_config"].update(json.load(f))
            pass

    def __getitem__(self, key):
        return self.__dict__["_config"][key]

    def __getattr__(self, attr):
        if attr in self.__dict__["_config"]:
            return self.__dict__["_config"][attr]

        raise AttributeError(f"No such {attr} in self._config")

    def get(self, key, default=None):
        return self.__dict__["_config"].get(key, default)

    def __setitem__(self, key, value):
        self.__dict__["_config"][key] = value

    def __setattr__(self, attr, value):
        self.__dict__["_config"][attr] = value

    def __contains__(self, item):
        return item in self.__dict__["_config"]

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __str__(self):
        return str(self.__dict__["_config"])

    def __repr__(self):
        return str(self.__dict__["_config"])

    def reset(self):
        self.__dict__["_config"] = copy.deepcopy(self._default_config)

    def update(self, *args, **kwargs):
        self.__dict__["_config"].update(*args, **kwargs)


ROOT_DIRPATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(os.path.dirname(ROOT_DIRPATH), "backend_data")
UPLOAD_PATH = os.path.join(DATA_PATH, "upload")
SQLITE_PATH = os.path.join(DATA_PATH, "database.db")
MARKET_PATH = os.path.join(DATA_PATH, "learnware")
PROPERTY_PATH = os.path.join(DATA_PATH, "property.json")

_DEFAULT_CONFIG = {
    # Global config
    "root_path": ROOT_DIRPATH,
    "upload_path": UPLOAD_PATH,
    "remove_upload_file": False,
    # Database config
    "database": {
        "type": "sqlalchemy",
        "url": f"sqlite:///{SQLITE_PATH}",
    },
    # Engine config
    "engine": {
        "type": "backend_market",
        "market_path": MARKET_PATH,
        "property_path": PROPERTY_PATH,
        "load_mode": "database",
    },
    # server config
    "listen_port": 8088,
    "listen_address": "0.0.0.0",
    # verify config
    "verify_timeout": 60 * 30,
    "backend_host": "127.0.0.1",
    # app config
    "app_secret_key": "my_secret_key",
    "email": {
        "smtp_server": "smtp.exmail.qq.com",
        "smtp_port": 465,
        "smtp_ssl": True,
        "smtp_username": "bm-support@lamda.nju.edu.cn",
        "smtp_password": "Learnware2023!",
        "sender_email": "bm-support@lamda.nju.edu.cn",
        "verification_url": "https://www.lamda.nju.edu.cn/learnware/#verify_email",
    },
}
