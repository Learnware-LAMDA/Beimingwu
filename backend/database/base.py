import enum


class LearnwareVerifyStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    WAITING = "WAITING"
    PROCESSING = "PROCESSING"
    QUEUE = "QUEUE"
    pass


class Database:
    def __init__(self):
        pass

    def install(
        self,
    ):
        raise NotImplementedError("'install' Method NOT Implemented.")

    def execute(self, sql, params=None):
        raise NotImplementedError("'query' Method NOT Implemented.")
