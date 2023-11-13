import os
import context
import unittest
import multiprocessing
from scripts import main
from context import config as C
import tempfile
import zipfile
import common_test_operations as testops
from learnware.config import C as learnware_config
from scripts.monitor_learnware_verify import verify_learnware_with_conda_checker


class TestVerifyLearnware(unittest.TestCase):
    def setUpClass() -> None:
        pass

    def tearDownClass() -> None:
        pass

    def test_verify_valid_learnware(self):
        learnware_path = os.path.join("tests", "data", "test_learnware.zip")
        semantic_spec = testops.test_learnware_semantic_specification_table()

        with tempfile.TemporaryDirectory() as tempdir:
            with zipfile.ZipFile(learnware_path, "r") as zip_ref:
                zip_ref.extractall(tempdir)
                pass

            verify_result, command_output = verify_learnware_with_conda_checker("00000test", tempdir, semantic_spec)
            pass

        print(command_output)
        self.assertTrue(verify_result)
        self.assertTrue(command_output.endswith("Success"))

        pass

    def test_verify_invalid_learnware(self):
        learnware_path = os.path.join("tests", "data", "test_learnware_invalid.zip")
        semantic_spec = testops.test_learnware_semantic_specification_table()

        with tempfile.TemporaryDirectory() as tempdir:
            with zipfile.ZipFile(learnware_path, "r") as zip_ref:
                zip_ref.extractall(tempdir)
                pass

            verify_result, command_output = verify_learnware_with_conda_checker("00000test", tempdir, semantic_spec)
            pass

        print(command_output)
        self.assertTrue(not verify_result)


if __name__ == "__main__":
    unittest.main()
