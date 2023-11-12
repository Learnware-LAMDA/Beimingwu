import unittest
import multiprocessing
import requests
import os
import sys
import time
import json
from learnware.client import LearnwareClient, SemanticSpecificationKey
from learnware.specification import Specification, RKMEStatSpecification

import tests.common_test_operations as testops
import lib.database_operations as dbops
from database.base import LearnwareVerifyStatus
import context
from scripts import main
import tempfile
import hashlib
import numpy as np


class TestLearnwareClient(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        testops.cleanup_folder()
        self.server_process = multiprocessing.Process(target=main.main)
        self.server_process.start()
        testops.wait_port_open(context.config.listen_port, 10)
        context.init_database()
        testops.clear_db()
        testops.url_request(
            "auth/register", {"username": "test", "password": "test", "email": "test@localhost", "confirm_email": False}
        )

        headers = testops.login("test@localhost", "test")
        result = testops.url_request(
            "user/create_token",
            {},
            headers=headers,
        )
        self.token = result["data"]["token"]

        self.backend_host = "http://localhost:{}".format(context.config.listen_port)

        pass

    def tearDown(self) -> None:
        super().tearDown()
        self.server_process.kill()
        self.server_process.join()
        testops.cleanup_folder()
        pass

    def test_upload_learnware(self):
        client = LearnwareClient(self.backend_host)

        client.login("test@localhost", self.token)
        learnware_id = client.upload_learnware(
            os.path.join("tests", "data", "test_learnware.zip"), testops.test_learnware_semantic_specification_table()
        )

        learnware_list = client.list_learnware()
        print(learnware_list)

        self.assertEqual(len(learnware_list), 1)
        with tempfile.NamedTemporaryFile(prefix="test_download_learnware_", suffix=".zip") as ftemp:
            client.download_learnware(learnware_id, ftemp.name)
            self.assertTrue(os.path.exists(ftemp.name))
            with open(ftemp.name, "rb") as fin, open(os.path.join("tests", "data", "test_learnware.zip"), "rb") as fref:
                self.assertEqual(hashlib.md5(fin.read()).hexdigest(), hashlib.md5(fref.read()).hexdigest())
                pass
            pass

        client.delete_learnware(learnware_id)
        pass

    def test_search_learnware(self):
        client = LearnwareClient(self.backend_host)
        client.login("test@localhost", self.token)
        learnware_id = client.upload_learnware(
            os.path.join("tests", "data", "test_learnware.zip"), testops.test_learnware_semantic_specification_table()
        )

        testops.add_learnware_to_engine(learnware_id, client.headers)

        specification = Specification()
        specification.update_semantic_spec(testops.test_learnware_semantic_specification_table())
        stat_spec = RKMEStatSpecification()
        stat_spec.load(os.path.join("tests", "data", "stat.json"))

        specification.update_stat_spec(stat_spec)
        learnware_list = client.search_learnware(specification)

        self.assertEqual(len(learnware_list), 1)
        self.assertEqual(learnware_list[0]["matching"], 1)
        client.delete_learnware(learnware_id)
        pass

    def test_search_learnware_no_stat(self):
        client = LearnwareClient(self.backend_host)
        client.login("test@localhost", self.token)
        learnware_id = client.upload_learnware(
            os.path.join("tests", "data", "test_learnware.zip"), testops.test_learnware_semantic_specification_table()
        )

        testops.add_learnware_to_engine(learnware_id, client.headers)

        specification = Specification()
        specification.update_semantic_spec(testops.test_learnware_semantic_specification_table())
        learnware_list = client.search_learnware(specification)

        self.assertEqual(len(learnware_list), 1)
        client.delete_learnware(learnware_id)
        pass

    def test_list_semantic_specification_values(self):
        client = LearnwareClient(self.backend_host)
        client.login("test@localhost", self.token)
        data_type_values = client.list_semantic_specification_values(SemanticSpecificationKey.DATA_TYPE)

        self.assertIn("Table", data_type_values)
        pass

    def test_load_learnware(self):
        client = LearnwareClient(self.backend_host)
        client.login("test@localhost", self.token)
        learnware_id = client.upload_learnware(
            os.path.join("tests", "data", "test_learnware.zip"), testops.test_learnware_semantic_specification_table()
        )

        testops.add_learnware_to_engine(learnware_id, client.headers)

        client.download_learnware(learnware_id, f"{learnware_id}.zip")
        learnware = client.load_learnware(f"{learnware_id}.zip", runnable_option="conda_env")
        os.remove(f"{learnware_id}.zip")

        learnware.instantiate_model()
        learnware_model = learnware.get_model()
        input_shape = learnware_model.input_shape
        inputs = np.random.randn(10, *input_shape)
        outputs = learnware.predict(inputs)

        client.delete_learnware(learnware_id)
        pass

    def test_check_learnware(self):
        client = LearnwareClient(self.backend_host)
        client.check_learnware(os.path.join("tests", "data", "test_learnware_multi_import.zip"))
        pass


if __name__ == "__main__":
    unittest.main()
