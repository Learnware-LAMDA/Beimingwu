import os
import copy

class Config:
    def __init__(self, default_conf):
        self.__dict__["_default_config"] = copy.deepcopy(default_conf)  # avoiding conflictions with __getattr__
        self.reset()

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
SQLITE_PATH  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files", "database.db")

_DEFAULT_CONFIG = {
    # Global config
    "root_path": ROOT_DIRPATH,
    
    # Database config
    "database_type": "sqlite",
    "sqlite_path": SQLITE_PATH,
    
    # Engine config
    "engine_type": "market", 
    
}

C = Config(_DEFAULT_CONFIG)
