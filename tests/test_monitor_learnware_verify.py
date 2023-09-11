

import unittest
from scripts import main, monitor_learnware_verify
import multiprocessing
import context
import requests
import os
import shutil
from tests import common_test_operations as testops
import lib.database_operations as dbops
from database.base import LearnwareVerifyStatus
import time
import json
import tempfile
import zipfile
import yaml


class TestMonitorLearnwareVerify(unittest.TestCase):

    def setUpClass() -> None:
        unittest.TestCase.setUpClass()

        TestMonitorLearnwareVerify.server_process = multiprocessing.Process(target=main.main)
        TestMonitorLearnwareVerify.server_process.start()

        testops.wait_port_open(context.config.listen_port, 10)
        context.init_database()
        testops.clear_db()
        TestMonitorLearnwareVerify.monitor_process = multiprocessing.Process(
            target=monitor_learnware_verify.main, args=(2,))
        TestMonitorLearnwareVerify.monitor_process.start()
        
        TestMonitorLearnwareVerify.username = 'test'
        TestMonitorLearnwareVerify.email = 'test@localhost'
        TestMonitorLearnwareVerify.password = 'test'
        testops.url_request(
            'auth/register', 
            {'username': TestMonitorLearnwareVerify.username, 
             'password': TestMonitorLearnwareVerify.password, 
             "email": TestMonitorLearnwareVerify.email,
             "confirm_email": False})


    def tearDownClass() -> None:
        unittest.TestCase.tearDownClass()
        TestMonitorLearnwareVerify.server_process.kill()
        TestMonitorLearnwareVerify.monitor_process.kill()
        pass

    def test_add_valid_learnware(self):
        headers = testops.login(TestMonitorLearnwareVerify.email, TestMonitorLearnwareVerify.password)
        learnware_id = testops.add_test_learnware_unverified(
            TestMonitorLearnwareVerify.email, TestMonitorLearnwareVerify.password)

        status = self.wait_verify_end(learnware_id)

        self.assertEqual(status, LearnwareVerifyStatus.SUCCESS.value)
        self.assertFalse(
            os.path.exists(context.get_learnware_verify_file_path(learnware_id)))
        
        result = testops.url_request(
            'user/list_learnware',
            {'page': 0, 'limit': 10},
            headers=headers
        )

        self.assertEqual(result['code'], 0)
        self.assertEqual(result['data']['total_pages'], 1)
        self.assertEqual(result['data']['learnware_list'][0]['learnware_id'], learnware_id)
        
        with tempfile.NamedTemporaryFile() as f:
            testops.download_learnware(learnware_id, headers, f.name)
            with zipfile.ZipFile(f.name, 'r') as zip_ref:
                f = zip_ref.open('learnware.yaml', 'r')
                learnware_info = yaml.safe_load(f)
                f.close()

                self.assertEqual(learnware_info['id'], learnware_id)
                
                fsmantic = zip_ref.open(learnware_info['semantic_specification']['file_name'])
                json.load(fsmantic)
                fsmantic.close()
                pass
            pass

        testops.delete_learnware(learnware_id, headers)
        pass

    def test_add_invalid_learnware(self):
        headers = testops.login(TestMonitorLearnwareVerify.email, TestMonitorLearnwareVerify.password)
        learnware_id = testops.add_test_learnware_unverified(
            TestMonitorLearnwareVerify.email, TestMonitorLearnwareVerify.password,
            learnware_filename='test_learnware_invalid.zip')

        status = self.wait_verify_end(learnware_id)

        self.assertEqual(status, LearnwareVerifyStatus.FAIL.value)
        self.assertTrue(
            os.path.exists(context.get_learnware_verify_file_path(learnware_id)))
        result = testops.url_request(
            'user/list_learnware_unverified',
            {'page': 0, 'limit': 10},
            headers=headers
        )

        self.assertEqual(result['code'], 0)
        self.assertEqual(result['data']['total_pages'], 1)
        self.assertEqual(len(result['data']['learnware_list']), 1)
        testops.delete_learnware(learnware_id, headers)
        pass

    def test_add_conda_learnware(self):
        headers = testops.login(TestMonitorLearnwareVerify.email, TestMonitorLearnwareVerify.password)
        learnware_id = testops.add_test_learnware_unverified(
            TestMonitorLearnwareVerify.email, TestMonitorLearnwareVerify.password,
            learnware_filename='test_learnware_conda.zip')

        status = self.wait_verify_end(learnware_id)

        self.assertEqual(status, LearnwareVerifyStatus.SUCCESS.value)
        self.assertFalse(
            os.path.exists(context.get_learnware_verify_file_path(learnware_id)))
        result = testops.url_request(
            'user/list_learnware',
            {'page': 0, 'limit': 10},
            headers=headers
        )

        self.assertEqual(result['code'], 0)
        self.assertEqual(result['data']['total_pages'], 1)
        self.assertEqual(result['data']['learnware_list'][-1]['learnware_id'], learnware_id)

        testops.delete_learnware(learnware_id, headers)

        pass

    
    def add_test_learnware(self, headers, input_dim, output_dim, filename='test_learnware.zip'):
        semantic_specification = testops.test_learnware_semantic_specification_table()
        semantic_specification['Input']['Dimension'] = input_dim
        semantic_specification['Output']['Dimension'] = output_dim

        learnware_file = open(
            os.path.join('tests', 'data', filename),'rb')
        files = {'learnware_file': learnware_file}

        # print(semantic_specification)
        semantic_specification['Input'] = json.dumps(semantic_specification['Input'])
        semantic_specification['Output'] = json.dumps(semantic_specification['Output'])

        result = testops.url_request(
            'user/add_learnware',
            {'semantic_specification': json.dumps(semantic_specification)},
            files=files,
            headers=headers
        )

        learnware_file.close()
        
        return result

    def wait_verify_end(self, learnware_id):
        for i in range(10):
            status = dbops.get_learnware_verify_status(learnware_id)

            if status == LearnwareVerifyStatus.PROCESSING.value:
                break

            time.sleep(1)
            pass
        
        self.assertEqual(status, LearnwareVerifyStatus.PROCESSING.value)

        for i in range(30 * 60):
            status = dbops.get_learnware_verify_status(learnware_id)
            if status != LearnwareVerifyStatus.PROCESSING.value:
                break
            time.sleep(1)
            pass

        return status

    def test_add_table_learnware(self):
        headers = testops.login(TestMonitorLearnwareVerify.email, TestMonitorLearnwareVerify.password)
        result = self.add_test_learnware(
            headers, input_dim=64, output_dim=10)

        self.assertEqual(result['code'], 0)
        learnware_id = result['data']['learnware_id']

        status = self.wait_verify_end(learnware_id)
        self.assertEqual(status, LearnwareVerifyStatus.SUCCESS.value)
        self.assertFalse(
            os.path.exists(context.get_learnware_verify_file_path(learnware_id)))
        result = testops.url_request(
            'user/list_learnware',
            {'page': 0, 'limit': 10},
            headers=headers
        )

        self.assertEqual(result['code'], 0)
        self.assertEqual(result['data']['total_pages'], 1)
        self.assertEqual(result['data']['learnware_list'][-1]['learnware_id'], learnware_id)

        testops.delete_learnware(learnware_id, headers)        
        pass

    def test_add_table_learnware_fail(self):
        headers = testops.login(TestMonitorLearnwareVerify.email, TestMonitorLearnwareVerify.password)

        result = self.add_test_learnware(
            headers, input_dim=63, output_dim=10)
    
        self.assertEqual(result['code'], 51)
        pass


    def test_add_folder_learnware(self):
        headers = testops.login(TestMonitorLearnwareVerify.email, TestMonitorLearnwareVerify.password)
        result = self.add_test_learnware(
            headers, input_dim=64, output_dim=10, filename='test_learnware_folder.zip')

        self.assertEqual(result['code'], 0)
        learnware_id = result['data']['learnware_id']

        status = self.wait_verify_end(learnware_id)
        self.assertEqual(status, LearnwareVerifyStatus.SUCCESS.value)
        self.assertFalse(
            os.path.exists(context.get_learnware_verify_file_path(learnware_id)))
        result = testops.url_request(
            'user/list_learnware',
            {'page': 0, 'limit': 10},
            headers=headers
        )

        self.assertEqual(result['code'], 0)
        self.assertEqual(result['data']['total_pages'], 1)
        self.assertEqual(result['data']['learnware_list'][-1]['learnware_id'], learnware_id)

        testops.delete_learnware(learnware_id, headers)        
        pass
    

if __name__ == '__main__':
    unittest.main()

