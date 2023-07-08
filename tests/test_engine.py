
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
import json
import zipfile


class TestEngine(unittest.TestCase):

    def setUpClass() -> None:
        unittest.TestCase.setUpClass()
        TestEngine.server_process = multiprocessing.Process(target=main.main)
        TestEngine.server_process.start()
        testops.wait_port_open(C.listen_port, 10)
        context.init_database()
        testops.clear_db()
        testops.url_request(
            'auth/register', 
            {'username': 'test', 'password': 'test', "email": "test@localhost"})
        TestEngine.learnware_id = testops.add_test_learnware('test@localhost', 'test')

    def tearDownClass() -> None:
        unittest.TestCase.tearDownClass()
        TestEngine.server_process.kill()
        pass

    
    def login(self):
        return testops.login('test@localhost', 'test')


    def test_semantic_specification(self):
        headers = self.login()
        result = testops.url_request(
            'engine/semantic_specification', 
            {}, headers=headers, method='get')

        self.assertEqual(result['code'], 0)
        
        pass

    def test_search_learnware(self):
        headers = self.login()
        sematic_specification = testops.test_learnware_semantic_specification()

        test_learnware_path = os.path.join('tests', 'data', 'test_learnware.zip')

        with zipfile.ZipFile(test_learnware_path, 'r') as zip_ref:
            zip_ref.extract('stat.json', os.path.join('tests','data'))
            pass
        
        stat_file = open(os.path.join('tests', 'data', 'stat.json'), 'rb')
        result = testops.url_request(
            'engine/search_learnware', 
            {'semantic_specification': json.dumps(sematic_specification)}, 
            files={'statistical_specification': stat_file},
            headers=headers)
        
        stat_file.close()
        os.remove(os.path.join('tests', 'data', 'stat.json'))
        # print(result)
        self.assertEqual(result['code'], 0)
        self.assertGreaterEqual(len(result['data']['learnware_list_single']), 1)
        self.assertEqual(result['data']['learnware_list_single'][-1]['learnware_id'], TestEngine.learnware_id)
        
        pass

    def test_download_learnware(self):
        headers = self.login()
        result = testops.url_request(
            'engine/download_learnware', 
            {'learnware_id': TestEngine.learnware_id}, 
            headers=headers, method='get', return_response=True)
        
        downloaded_filename = os.path.join('tests', 'data', 'download_learnware.zip')
        with open(downloaded_filename, 'wb') as f:
            f.write(result.content)
            pass

        learnware_filename = os.path.join('tests', 'data', 'test_learnware.zip')
        self.assertEqual(
            os.path.getsize(downloaded_filename),
            os.path.getsize(learnware_filename)
        )

        os.remove(downloaded_filename)
        pass

    def test_learnware_info(self):
        headers = self.login()

        result = testops.url_request(
            'engine/learnware_info', 
            {'learnware_id': TestEngine.learnware_id}, 
            headers=headers, method='get')
        
        self.assertEqual(result['code'], 0)

        self.assertEqual(
            result['data']['learnware_info']['semantic_specification']['Name'],
            testops.test_learnware_semantic_specification()['Name']
        )
        pass


if __name__ == '__main__':
    unittest.main()

