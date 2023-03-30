import sqlite3
from config import C
from .base import Database
import os

__all__ = ["SQLite"]

class SQLite(Database):

    USER_INTALL_SQL = '''
    CREATE TABLE user
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role INTEGER DEFAULT 0 NOT NULL,
        nickname TEXT NOT NULL,
        register INTEGER NOT NULL,
        last_login INTEGER 
    );
    '''
    
    LEARNWARE_INSTALL_SQL = '''
    CREATE TABLE user_learnware_raltion
    (
        user_id INTEGER NOT NULL,
        learnware_id TEXT UNIQUE NOT NULL,
        last_modify INTEGER,
        FOREIGN KEY (user_id) REFERENCES user(id)
    );
    '''
    
    DATASET_INIT_DATA = [
        "INSERT INTO user (username, nickname, email, password, role, register) VALUES ('tanzh',  'TanZH', 'tanzh@lamda.nju.edu.cn', 'Qwerty123', 1, strftime('%s'))",
        "INSERT INTO user (username, nickname, email, password, role, register) VALUES ('tanp',   'TanP',  'tanp@lamda.nju.edu.cn',  'Qwerty123', 1, strftime('%s'))",
        "INSERT INTO user (username, nickname, email, password, role, register) VALUES ('guolz',  'GuoLZ', 'guolz@lamda.nju.edu.cn', 'Qwerty123', 1, strftime('%s'))",
        "INSERT INTO user (username, nickname, email, password, register) VALUES ('zhouz', 'ZhouZ', 'zhouz@lamda.nju.edu.cn', 'Qwerty123', strftime('%s'))",
        "INSERT INTO user (username, nickname, email, password, register) VALUES ('jinyx', 'JinYX', 'jinyx@lamda.nju.edu.cn', 'Qwerty123', strftime('%s'))",
    ]
    
    def __init__(self, path: str):
        self.path = path
        self.install()
    
    def install(self, ):
        if os.path.exists(self.path): return 
        if not os.path.exists(os.path.dirname(self.path)): os.makedirs(os.path.dirname(self.path))
        self.query(self.USER_INTALL_SQL)
        self.query(self.LEARNWARE_INSTALL_SQL)
        for sql in self.DATASET_INIT_DATA:
            self.query(sql)
    
    def query(self, sql, params=None):
        # Build connection
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        # Execute SQL
        if params is None:
            cursor = c.execute(sql)
        else:
            cursor = c.execute(sql, params)
        # Collect result
        ret_cnt, ret = conn.total_changes, []
        while cursor is not None:
            res = cursor.fetchone()
            if res is None: break
            ret.append(res)
        # Coda
        conn.commit()
        conn.close()
        return ret_cnt, ret
