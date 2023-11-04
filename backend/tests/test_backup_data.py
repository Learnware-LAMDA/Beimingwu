import os
import unittest
from scripts import backup_data
import common_test_operations as testops
from learnware.config import C as learnware_config


class TestBackupData(unittest.TestCase):
    def setUp(
        self,
    ) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()
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
