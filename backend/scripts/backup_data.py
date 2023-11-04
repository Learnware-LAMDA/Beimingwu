import context
import database.sqlalchemy
import os
from learnware.config import C as learnware_config
import shutil
import sys
from datetime import datetime

MARKET_ID = "default"


def backup_backend_database(backup_path: str):
    database_url = context.config["database"]["url"]
    backup_filename = os.path.join(backup_path, "backend.sql")
    helper = database.sqlalchemy.DatabaseHelper.create_from_url(database_url)
    helper.dump_database(database_url, backup_filename)
    pass


def backup_learnware_database(backup_path: str):
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
    helper.dump_database(database_url, backup_filename)
    pass


def backup_backend_folder(backup_path: str):
    upload_folder_name = os.path.basename(context.config["upload_path"])
    shutil.copytree(context.config["upload_path"], os.path.join(backup_path, upload_folder_name))
    pass


def backup_learnware_folder(backup_path: str):
    learnware_path = os.path.join(learnware_config["market_root_path"], MARKET_ID, "learnware_pool")
    learnware_folder_name = os.path.basename(learnware_path)
    shutil.copytree(learnware_path, os.path.join(backup_path, learnware_folder_name))
    pass


def main():
    backup_path = os.path.join(context.config["backup_path"], datetime.now().strftime("%Y%m%d%H%M%S"))

    os.makedirs(backup_path, exist_ok=True)
    backup_backend_database(backup_path)
    backup_learnware_database(backup_path)
    backup_backend_folder(backup_path)
    backup_learnware_folder(backup_path)

    max_backup_count = context.config["backup_max_count"]
    backup_folders = [f for f in os.listdir(context.config["backup_path"]) if not f.startswith(".")]
    backup_folders.sort(reverse=True)
    backup_folders = backup_folders[max_backup_count:]
    for folder in backup_folders:
        shutil.rmtree(os.path.join(context.config["backup_path"], folder))
        pass
    pass


if __name__ == "__main__":
    main()
    pass
