import sqlite3
from config import C
from .base import Database


__all__ = ["SQLite"]

class SQLite(Database):
    def __init__(self, path):
        self.path = path
    
    def install(self, ):
        raise NotImplementedError("'install' Method NOT Implemented.")
        
    def query(self, sql, params):
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
