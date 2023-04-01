from config import C

COLUMNS_USER = ["id", "username", "password", "email", "role", "nickname", "register", "last_login"]
COLUMNS_LEARNWARE = ["user_id", "learnware_id", "last_modify"]

def check_user_exist(by, value):
    ret_cnt, ret = C.database.query(f"SELECT {by} FROM user WHERE {by} = ?", (value,))
    return len(ret) > 0


def get_user_info(by, value):
    ret_cnt, ret = C.database.query(f"SELECT * FROM user WHERE {by} = ?", (value,))
    return dict(zip(COLUMNS_USER, ret[0])) if len(ret) > 0 else None


def add_user(username, password, email, role, nickname):
    ret_cnt, _ = C.database.query(
        'INSERT INTO user (username, password, email, role, nickname, register) VALUES (?, ?, ?, ?, ?, strftime("%s"))',
        (username, password, email, role, nickname),
    )
    return ret_cnt > 0

def get_learnware_list(by, value):
    ret_cnt, ret = C.database.query(f"SELECT * FROM user_learnware_relation WHERE {by} = ?", (value,))
    return [ dict(zip(COLUMNS_LEARNWARE, ret[i])) for i in range(len(ret)) ]

def add_learnware(user_id, learnware_id):
    ret_cnt, ret = C.database.query(
        'INSERT INTO user_learnware_relation (user_id, learnware_id, last_modify) VALUES(?, ?, strftime("%s"))', 
        (user_id, learnware_id)
    )
    return ret_cnt

def remove_learnware(by, value):
    ret_cnt, ret = C.database.query(f"DELETE FROM user_learnware_relation WHERE {by} = ?", (value,))
    return ret_cnt

def remove_user(by, value):
    ret_cnt, ret = C.database.query(f"DELETE FROM user WHERE {by} = ?", (value,))
    return ret_cnt

def get_all_user_list(columns):
    column_str = ", ".join(columns)
    ret_cnt, ret = C.database.query(f"SELECT {column_str} FROM user")
    return [dict(zip(columns, user)) for user in ret]

def get_all_learnware_list(columns):
    column_str = ", ".join(columns)
    ret_cnt, ret = C.database.query(f"SELECT {column_str} FROM user_learnware_relation")
    return [dict(zip(columns, user)) for user in ret]


