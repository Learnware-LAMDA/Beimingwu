import unittest
import multiprocessing
import requests
import os
import sys
import time
import json
from learnware.client import LearnwareClient
from learnware.specification import Specification, RKMEStatSpecification

import tests.common_test_operations as testops
import lib.database_operations as dbops
from database.base import LearnwareVerifyStatus
import context
from scripts import main
import tempfile
import hashlib


class TestLearnwareClient(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.server_process = multiprocessing.Process(target=main.main)
        self.server_process.start()
        testops.wait_port_open(context.config.listen_port, 10)
        context.init_database()
        testops.clear_db()
        testops.url_request(
            'auth/register', 
            {'username': 'test', 'password': 'test', "email": "test@localhost"})
        self.backend_host = 'http://localhost:{}'.format(context.config.listen_port)

        pass
    
    def tearDown(self) -> None:
        super().tearDown()
        self.server_process.kill()
        pass


    def test_upload_learnware(self):
        client = LearnwareClient(self.backend_host)

        client.login('test@localhost', 'test', hash_password=False)
        learnware_id = client.upload_learnware(
            testops.test_learnware_semantic_specification_table(),
            os.path.join('tests', 'data', 'test_learnware.zip'))
        
        learnware_list = client.list_learnware()
        print(learnware_list)

        self.assertEqual(len(learnware_list), 1)
        with tempfile.NamedTemporaryFile(prefix="test_download_learnware_", suffix=".zip") as ftemp:
            client.download_learnware(learnware_id, ftemp.name)
            self.assertTrue(os.path.exists(ftemp.name))
            with open(ftemp.name, 'rb') as fin, open(os.path.join('tests', 'data', 'test_learnware.zip'), 'rb') as fref:
                self.assertEqual(
                    hashlib.md5(fin.read()).hexdigest(), 
                    hashlib.md5(fref.read()).hexdigest())
                pass
            pass

        client.delete_learnware(learnware_id)
        pass

    def test_search_learnware(self):
        client = LearnwareClient(self.backend_host)
        client.login('test@localhost', 'test', hash_password=False)
        learnware_id = client.upload_learnware(
            testops.test_learnware_semantic_specification_table(),
            os.path.join('tests', 'data', 'test_learnware.zip'))

        testops.add_learnware_to_engine(learnware_id, client.headers)

        specification = Specification()
        specification.upload_semantic_spec(testops.test_learnware_semantic_specification_table())
        stat_spec = RKMEStatSpecification()
        stat_spec.load(os.path.join('tests', 'data', 'stat.json'))

        specification.update_stat_spec(test_spec=stat_spec)
        learnware_list = client.search_learnware(specification)

        self.assertEqual(len(learnware_list), 1)
        self.assertEqual(learnware_list[0]['matching'], 1)
        client.delete_learnware(learnware_id)
        pass

    def test_search_learnware_no_stat(self):
        client = LearnwareClient(self.backend_host)
        client.login('test@localhost', 'test', hash_password=False)
        learnware_id = client.upload_learnware(
            testops.test_learnware_semantic_specification_table(),
            os.path.join('tests', 'data', 'test_learnware.zip'))

        testops.add_learnware_to_engine(learnware_id, client.headers)

        specification = Specification()
        specification.upload_semantic_spec(testops.test_learnware_semantic_specification_table())
        learnware_list = client.search_learnware(specification)

        self.assertEqual(len(learnware_list), 1)
        client.delete_learnware(learnware_id)
        pass


if __name__ == '__main__':
    unittest.main()