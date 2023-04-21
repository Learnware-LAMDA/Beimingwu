from config import C

COLUMNS_USER = ["id", "username", "password", "email", "role", "nickname", "register", "last_login"]
COLUMNS_LEARNWARE = ["user_id", "learnware_id", "last_modify"]


def check_user_exist(by, value):
    ret_cnt, ret = C.database.query(f"SELECT {by} FROM user WHERE {by} = ?", (value,))
    return len(ret) > 0


def get_user_info(by, value):
    ret_cnt, ret = C.database.query(f"SELECT * FROM user WHERE {by} = ?", (value,))
    return dict(zip(COLUMNS_USER, ret[0])) if len(ret) > 0 else None

def update_user_password(by, value, pwd):
    ret_cnt, ret = C.database.query(f"UPDATE user SET password = ? WHERE {by} = ?", (pwd, value,))
    return ret_cnt > 0

def add_user(username, password, email, role, nickname):
    ret_cnt, _ = C.database.query(
        'INSERT INTO user (username, password, email, role, nickname, register) VALUES (?, ?, ?, ?, ?, strftime("%s"))',
        (username, password, email, role, nickname),
    )
    return ret_cnt > 0


def get_learnware_list(by, value, limit=None, page=None):
    _, cnt = C.database.query(f"SELECT COUNT(*) FROM user_learnware_relation WHERE {by} = ?", (value,))
    suffix = "" if limit is None or page is None else f"LIMIT {limit} OFFSET {limit * page}"
    _, ret = C.database.query(f"SELECT * FROM user_learnware_relation WHERE {by} = ? {suffix}", (value,))
    return [dict(zip(COLUMNS_LEARNWARE, ret[i])) for i in range(len(ret))], cnt[0][0]

def add_learnware(user_id, learnware_id):
    ret_cnt, ret = C.database.query(
        'INSERT INTO user_learnware_relation (user_id, learnware_id, last_modify) VALUES(?, ?, strftime("%s"))',
        (user_id, learnware_id),
    )
    return ret_cnt


def remove_learnware(by, value):
    ret_cnt, ret = C.database.query(f"DELETE FROM user_learnware_relation WHERE {by} = ?", (value,))
    return ret_cnt


def remove_user(by, value):
    ret_cnt, ret = C.database.query(f"DELETE FROM user WHERE {by} = ?", (value,))
    return ret_cnt


def get_all_user_list(columns, limit=None, page=None, username=None, email=None):
    column_str = ", ".join(columns)
    _, cnt = C.database.query(f"SELECT COUNT(*) FROM user")
    like_suffix = ""
    if username is not None or email is not None:
        if username is None or email is None:
            like_suffix = "WHERE "
            if username is not None: like_suffix += f"username LIKE '%{username}%'"
            if email is not None: like_suffix += f"email LIKE '%{email}%'"
        else:
            like_suffix = f"WHERE username LIKE '%{username}%' AND email LIKE '%{email}%'"
    page_suffix = "" if limit is None or page is None else f"LIMIT {limit} OFFSET {limit * page}"
    _, ret = C.database.query(f"SELECT {column_str} FROM user {like_suffix} {page_suffix}")
    return [dict(zip(columns, user)) for user in ret], cnt[0][0]


def get_all_learnware_list(columns, limit=None, page=None):
    column_str = ", ".join(columns)
    _, cnt = C.database.query(f"SELECT COUNT(*) FROM user_learnware_relation")
    suffix = "" if limit is None or page is None else f"LIMIT {limit} OFFSET {limit * page}"
    _, ret = C.database.query(f"SELECT {column_str} FROM user_learnware_relation {suffix}")
    return [dict(zip(columns, user)) for user in ret], cnt[0][0]
