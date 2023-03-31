from config import C
    
COLUMNS_USER = ['id', 'username', 'password', 'email', 'role', 'nickname', 'register', 'last_login']


def check_user_exist(by, value):
    ret_cnt, ret = C.database.query(f'SELECT {by} FROM user WHERE {by} = ?', (value, ))
    return len(ret) > 0


def get_user_info(by, value):
    ret_cnt, ret = C.database.query(f'SELECT * FROM user WHERE {by} = ?', (value, ))
    return dict(zip(COLUMNS_USER, ret[0])) if len(ret) > 0 else None


def add_user(username, password, email, role, nickname):
    ret_cnt, _ = C.database.query('INSERT INTO user (username, password, email, role, nickname, register) VALUES (?, ?, ?, ?, ?, strftime("%s"))', (username, password, email, role, nickname))
    return ret_cnt > 0


def get_all_user_info(columns):
    column_str = ', '.join(columns)
    ret_cnt, ret = C.database.query(f"SELECT {column_str} FROM user")
    return [dict(zip(columns, user)) for user in ret]
