
__all__ = ["Database"]

class Database:
    def __init__(self):
        pass
    
    def install(self,):
        raise NotImplementedError("'install' Method NOT Implemented.")
    
    def query(self, sql, params):
        raise NotImplementedError("'query' Method NOT Implemented.")