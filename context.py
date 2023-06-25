'''context.py: All globals should be defined here.

'''
from config import Config
from database import Database, SQLAlchemy

database : Database = None
engine = None
stats = 0

config = Config()

def init_database(admin_password: str = None):
    global config, database

    if config.database['type'] == "sqlalchemy":
        database = SQLAlchemy(config=config.database, admin_password=admin_password)
        pass
    
    if database is None:
        raise ValueError(f"Database type {config.database['type']} is not supproted.")
    pass