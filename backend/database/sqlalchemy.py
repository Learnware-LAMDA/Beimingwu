from .base import Database, LearnwareVerifyStatus
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text
from sqlalchemy import Column, Integer, Text, DateTime, String, PrimaryKeyConstraint, UniqueConstraint, Index

from datetime import datetime


__all__ = ["SQLAlchemy"]

DeclarativeBase = declarative_base()


class User(DeclarativeBase):
    __tablename__ = "tb_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    role = Column(Integer, server_default=text("0"), nullable=False)
    nickname = Column(Text, nullable=False)
    register = Column(DateTime, nullable=False)
    last_login = Column(DateTime, nullable=True)
    email_confirm_time = Column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint(username), UniqueConstraint(email), {})
    pass


class UserLearnwareRelation(DeclarativeBase):
    __tablename__ = "tb_user_learnware_relation"

    user_id = Column(Integer, nullable=False)
    learnware_id = Column(Text, nullable=False)
    last_modify = Column(DateTime, nullable=False)
    verify_status = Column(
        String(10), nullable=False, server_default=text(LearnwareVerifyStatus.WAITING.value), index=True
    )
    verify_log = Column(Text, nullable=True)

    __table_args__ = (PrimaryKeyConstraint(user_id, learnware_id), {})
    pass


class GlobalCounter(DeclarativeBase):
    __tablename__ = "tb_global_counter"

    name = Column(Text, nullable=False)
    value = Column(Integer, nullable=False)

    __table_args__ = (PrimaryKeyConstraint(name), {})
    pass


class UserToken(DeclarativeBase):
    __tablename__ = "tb_user_token"

    user_id = Column(Integer, nullable=False, index=True)
    token = Column(Text, nullable=False)

    __table_args__ = (PrimaryKeyConstraint(user_id, token), {})
    pass


class Log(DeclarativeBase):
    __tablename__ = "tb_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, nullable=False)
    name = Column(String(255), nullable=False)
    info = Column(Text, nullable=True)

    __table_args__ = (Index("idx_name_create_time", name, create_time), {})
    pass


class DatabaseHelper(object):
    def database_exists(self):
        raise NotImplementedError()

    def create_database(self):
        raise NotImplementedError()

    pass


class PostgresHelper(DatabaseHelper):
    def get_engine_no_dbname(self, url: str):
        dbname_start = url.rfind("/")
        dbname = url[dbname_start + 1 :]

        url_no_dbname = url[:dbname_start] + "/postgres"

        engine = create_engine(url_no_dbname)

        return engine, dbname

    def database_exists(self, url: str) -> bool:
        engine, dbname = self.get_engine_no_dbname(url)

        with engine.connect() as conn:
            result = conn.execute(text("SELECT datname FROM pg_database;"))
            db_list = set()

            for row in result.fetchall():
                db_list.add(row[0].lower())
                pass

            if dbname.lower() not in db_list:
                return False
            else:
                return True
            pass
        pass

    def create_database(self, url):
        engine, dbname = self.get_engine_no_dbname(url)
        with engine.connect() as conn:
            conn.execution_options(isolation_level="AUTOCOMMIT").execute(text("CREATE DATABASE {0};".format(dbname)))
            pass
        pass


class SqliteHelper(DatabaseHelper):
    def get_path(self, url: str):
        start = url.find(":///")
        return url[start + 4 :]

    def database_exists(self, url: str) -> bool:
        path = self.get_path(url)

        if os.path.exists(path):
            return True
        else:
            return False
        pass

    def create_database(self, url: str):
        path = self.get_path(url)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        pass


class SQLAlchemy(Database):

    DATASET_INIT_DATA = [
        "INSERT INTO tb_user (username, nickname, email, password, role, register, email_confirm_time) VALUES ('admin',  'adminitrator', 'admin@localhost', :admin_password, 1, :now, :now)",
        "INSERT INTO tb_global_counter (name, value) VALUES ('learnware_id', 0)",
    ]

    def __init__(self, config, admin_password):
        self.url = config["url"]
        self.install(admin_password)
        pass

    def install(self, admin_password):
        if self.url.startswith("sqlite"):
            helper = SqliteHelper()
        elif self.url.startswith("postgresql"):
            helper = PostgresHelper()
        else:
            raise Exception(f"Unsupported database url: {self.url}")
            pass

        if not helper.database_exists(self.url):
            if admin_password is None:
                raise RuntimeError("admin password is required for creating database")

            helper.create_database(self.url)
            self.engine = create_engine(self.url, future=True)

            # create all tables
            DeclarativeBase.metadata.create_all(self.engine)

            for sql in self.DATASET_INIT_DATA:
                self.execute(sql, {"admin_password": admin_password, "now": datetime.now()})
                pass
            pass

        else:
            self.engine = create_engine(self.url, future=True)
            pass

    def execute(self, sql, params=None, conn=None):
        if conn is None:
            conn_ = self.engine.connect()
            pass
        else:
            conn_ = conn
            pass

        try:
            if params is None:
                result = conn_.execute(text(sql))
            else:
                result = conn_.execute(text(sql), params)
                pass

            if result.returns_rows:
                rows = result.fetchall()
            else:
                rows = None

            if conn is None:
                conn_.commit()
                pass
        finally:
            if conn is None:
                conn_.close()
                pass
            pass

        return rows

    def begin(self):
        return self.engine.begin()
