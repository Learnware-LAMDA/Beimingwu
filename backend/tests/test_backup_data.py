import os
import context
import unittest
import multiprocessing
from scripts import main
from context import config as C
from scripts import backup_data
import common_test_operations as testops
from learnware.config import C as learnware_config


class TestBackupData(unittest.TestCase):
    def setUpClass() -> None:
        testops.cleanup_folder()
        unittest.TestCase.setUpClass()
        TestBackupData.server_process = multiprocessing.Process(target=main.main)
        TestBackupData.server_process.start()
        testops.wait_port_open(C.listen_port, 10)
        context.init_database()
        testops.clear_db()
        testops.url_request(
            "auth/register", {"username": "test", "password": "test", "email": "test@localhost", "confirm_email": False}
        )

    def tearDownClass() -> None:
        unittest.TestCase.tearDownClass()
        headers = testops.login("test@localhost", "test")
        TestBackupData.server_process.kill()
        testops.cleanup_folder()
        pass

    def test_run_backup(self):
        backup_folder = testops.context.config["backup_path"]
        upload_path = testops.context.config["upload_path"]
        learnware_path = os.path.join(learnware_config["market_root_path"], "default", "learnware_pool")
        upload_folder_name = os.path.basename(upload_path)
        learnware_folder_name = os.path.basename(learnware_path)
        if os.path.exists(backup_folder):
            os.system(f"rm -rf {backup_folder}/*")
            pass

        os.system(f"echo 'test' > {upload_path}/test.txt")
        os.system(f"echo 'test' > {learnware_path}/test.txt")

        backup_data.main()
        backup_name = [f for f in os.listdir(backup_folder) if not f.startswith(".")][0]
        backup_path = os.path.join(backup_folder, backup_name)

        self.assertTrue(os.path.exists(os.path.join(backup_path, "backend.sql")))
        self.assertTrue(os.path.exists(os.path.join(backup_path, "learnware.sql")))
        self.assertTrue(os.path.exists(os.path.join(backup_path, upload_folder_name, "test.txt")))
        self.assertTrue(os.path.exists(os.path.join(backup_path, learnware_folder_name, "test.txt")))
        pass


if __name__ == "__main__":
    unittest.main()
