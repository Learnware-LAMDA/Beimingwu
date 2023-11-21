import context
import database.sqlalchemy
import os
from learnware.config import C as learnware_config
import shutil
import sys
from datetime import datetime

MARKET_ID = "default"


def restore_backend_database(backup_path: str):
    database_url = context.config["database"]["url"]
    backup_filename = os.path.join(backup_path, "backend.sql")
    helper = database.sqlalchemy.DatabaseHelper.create_from_url(database_url)
    helper.restore_database(database_url, backup_filename)
    pass


def restore_learnware_database(backup_path: str):
    database_url = learnware_config["database_url"]
    market_id = MARKET_ID
    if database_url.startswith("sqlite"):
        database_url = database_url + f"/market_{market_id}.db"
        pass
    else:
        database_url = database_url + f"/market_{market_id}"
        pass

    backup_filename = os.path.join(backup_path, "learnware.sql")
    helper = database.sqlalchemy.DatabaseHelper.create_from_url(database_url)
    helper.restore_database(database_url, backup_filename)
    pass


def restore_backend_folder(backup_path: str):
    upload_folder_name = os.path.basename(context.config["upload_path"])
    shutil.rmtree(context.config["upload_path"], ignore_errors=True)
    shutil.copytree(os.path.join(backup_path, upload_folder_name), context.config["upload_path"])
    pass


def restore_learnware_folder(backup_path: str):
    learnware_path = os.path.join(learnware_config["market_root_path"], MARKET_ID, "learnware_pool")
    learnware_folder_name = os.path.basename(learnware_path)
    shutil.rmtree(learnware_path, ignore_errors=True)
    shutil.copytree(os.path.join(backup_path, learnware_folder_name), learnware_path)
    pass


def main(backup_path):
    restore_backend_database(backup_path)
    restore_learnware_database(backup_path)
    restore_backend_folder(backup_path)
    restore_learnware_folder(backup_path)
    pass


if __name__ == "__main__":
    main(sys.argv[1])
    pass
