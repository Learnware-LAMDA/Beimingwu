import unittest
from scripts import main
import multiprocessing
import context
from context import config as C
import requests
import os
import shutil
from tests import common_test_operations as testops
import time
import restful.utils as utils
import hashlib


class TestDatasets(unittest.TestCase):
    def setUpClass() -> None:
        testops.cleanup_folder()
        unittest.TestCase.setUpClass()
        testops.set_config("datasets_path", os.path.join("tests"))
        mp_context = multiprocessing.get_context("spawn")
        TestDatasets.server_process = mp_context.Process(target=main.main)
        TestDatasets.server_process.start()
        testops.wait_port_open(C.listen_port, 10)
        context.init_database()
        testops.clear_db()
        TestDatasets.username = "test"
        TestDatasets.email = "test@localhost"
        TestDatasets.password = "test"
        testops.url_request(
            "auth/register",
            {
                "username": TestDatasets.username,
                "password": TestDatasets.password,
                "email": TestDatasets.email,
                "confirm_email": False,
            },
        )

    def tearDownClass() -> None:
        unittest.TestCase.tearDownClass()
        TestDatasets.server_process.kill()
        testops.cleanup_folder()
        testops.reset_config()

    def test_list(self):
        headers = testops.login(TestDatasets.email, TestDatasets.password)
        result = testops.url_request("datasets/list_datasets", headers=headers)

        self.assertEqual(result["code"], 0)
        self.assertIn("data/stat.json", result["data"]["datasets"])

        pass

    def test_download(
        self,
    ):
        result = testops.url_request(
            "datasets/download_datasets", {"dataset": "data/stat.json"}, method="get", return_response=True
        )

        with open(os.path.join("tests", "data", "stat.json"), "rb") as fin:
            file_content = fin.read()
            pass
        self.assertTrue(testops.check_bytes_same(result.content, file_content))
        pass


if __name__ == "__main__":
    unittest.main()
