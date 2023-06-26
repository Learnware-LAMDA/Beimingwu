from typing import Tuple
from datetime import datetime
import context


def check_user_exist(by, value, conn=None):
    rows = context.database.execute(f"SELECT {by} FROM tb_user WHERE {by} = :{by}", {by: value}, conn=conn)

    if len(rows) == 0:
        return False
    else:
        return True


def get_user_info(by, value):
    rows = context.database.execute(f"SELECT * FROM tb_user WHERE {by} = :{by}", {by: value})
    if len(rows) == 0:
        return None
    else:
        return rows[0]._mapping


def update_user_password(by, value, pwd):
    context.database.execute(
        f"UPDATE tb_user SET password = :password WHERE {by} = :{by}", 
        {"password": pwd, by: value})
    return True


def add_user(username, password, email, role, nickname, conn=None):
    rows = context.database.execute(
        'INSERT INTO tb_user (username, password, email, role, nickname, register) VALUES (:username, :password, :email, :role, :nickname, :register) RETURNING id',
        {
            'username': username, 
            'password': password, 
            'email': email,
            'role': role,
            'nickname': nickname,
            'register': datetime.now()
        },
        conn=conn
    )
    return rows[0][0]


def register_user(username, password, email) -> Tuple[int, str]:
    '''all db ops in register user should in a session
    '''
    
    with begin() as conn:
        if check_user_exist(by="username", value=username, conn=conn):
            return 51, "Username already exist.", -1

        # Check uniqueness of email
        if check_user_exist(by="email", value=email, conn=conn):
            return 52, "Email already exist.", -1

        user_id = add_user(username, password, email, 0, username, conn=conn)
        if user_id is None:
            return 31, "System error.", -1
            pass
        
        conn.commit()
        return 0, 'success', user_id
    pass


def get_learnware_list(by, value, limit=None, page=None):
    cnt = context.database.execute(f"SELECT COUNT(*) FROM tb_user_learnware_relation WHERE {by} = :{by}", {by: value})

    suffix = "" if limit is None or page is None else f"LIMIT {limit} OFFSET {limit * page}"
    rows = context.database.execute(
        f"SELECT * FROM tb_user_learnware_relation WHERE {by} = :{by} {suffix}",
        {by: value})
    return [r._mapping for r in rows], cnt[0][0]


def add_learnware(user_id, learnware_id):
    context.database.execute(
        'INSERT INTO tb_user_learnware_relation (user_id, learnware_id, last_modify) VALUES(:user_id, :learnware_id, :last_modify)',
        {'user_id': user_id, 'learnware_id': learnware_id, 'last_modify': datetime.now()}
    )
    return 1


def get_learnware_owner(learnware_id):
    rows = context.database.execute(
        "SELECT username FROM tb_user WHERE id IN (SELECT user_id FROM tb_user_learnware_relation WHERE learnware_id = :learnware_id)",
        {"learnware_id": learnware_id}
    )
    if len(rows) == 0 or len(rows[0]) == 0: 
        return "Unknown"
    return rows[0][0]


def remove_learnware(by, value):
    context.database.execute(f"DELETE FROM tb_user_learnware_relation WHERE {by} = :{by}",
                     {by: value})
    return 1


def remove_user(by, value):
    context.database.execute(
        f"DELETE FROM tb_user WHERE {by} = :{by}",
        {by: value})
    return 1


def get_all_user_list(columns, limit=None, page=None, username=None, email=None):
    column_str = ", ".join(columns)
    cnt = context.database.execute(f"SELECT COUNT(*) FROM tb_user")
    like_suffix = ""
    if username is not None or email is not None:
        if username is None or email is None:
            like_suffix = "WHERE "
            if username is not None: like_suffix += f"username LIKE '%{username}%'"
            if email is not None: like_suffix += f"email LIKE '%{email}%'"
        else:
            like_suffix = f"WHERE username LIKE '%{username}%' AND email LIKE '%{email}%'"
    page_suffix = "" if limit is None or page is None else f"LIMIT {limit} OFFSET {limit * page}"
    rows = context.database.execute(f"SELECT {column_str} FROM tb_user {like_suffix} {page_suffix}")
    return [dict(zip(columns, user)) for user in rows], cnt[0][0]


def get_all_learnware_list(columns, limit=None, page=None):
    column_str = ", ".join(columns)
    cnt = context.database.execute(f"SELECT COUNT(*) FROM tb_user_learnware_relation")
    suffix = "" if limit is None or page is None else f"LIMIT {limit} OFFSET {limit * page}"
    ret = context.database.execute(f"SELECT {column_str} FROM tb_user_learnware_relation {suffix}")
    return [dict(zip(columns, user)) for user in ret], cnt[0][0]


def begin():
    return context.database.begin()