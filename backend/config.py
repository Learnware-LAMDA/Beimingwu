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
TEMP_PATH = os.path.join(DATA_PATH, "temp")
BACKUP_PATH = os.path.join(DATA_PATH, "backup")
SQLITE_PATH = os.path.join(DATA_PATH, "database.db")
MARKET_PATH = os.path.join(DATA_PATH, "learnware")
PROPERTY_PATH = os.path.join(DATA_PATH, "property.json")

_DEFAULT_CONFIG = {
    # Global config
    "root_path": ROOT_DIRPATH,
    "upload_path": UPLOAD_PATH,
    "temp_path": TEMP_PATH,
    "backup_path": BACKUP_PATH,
    "backup_max_count": 7,
    "remove_upload_file": False,
    "register_email_patterns": [""],
    # Database config
    "database": {
        "type": "sqlalchemy",
        "url": f"sqlite:///{SQLITE_PATH}",
    },
    # Engine config
    "engine": {
        "type": "hetero",
        "market_path": MARKET_PATH,
        "property_path": PROPERTY_PATH,
        "load_mode": "database",
    },
    # server config
    "listen_port": 8088,
    "listen_address": "0.0.0.0",
    # verify config
    "verify_timeout": 60 * 30,
    "verify_proxy": "",
    "backend_host": "127.0.0.1",
    # app config
    "app_secret_key": "my_secret_key",
    "email": {
        "smtp_server": "",
        "smtp_port": 465,
        "smtp_ssl": True,
        "smtp_username": "",
        "smtp_password": "",
        "sender_email": "",
        "verification_url": "",
        "reset_password_url": "",
        "proxy_host": "",
        "proxy_port": 0,
    },
    # redis config
    "redis": {"host": "127.0.0.1", "port": 6379},
}
