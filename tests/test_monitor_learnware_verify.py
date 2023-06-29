

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
             "email": TestMonitorLearnwareVerify.email})


    def tearDownClass() -> None:
        unittest.TestCase.tearDownClass()
        TestMonitorLearnwareVerify.server_process.kill()
        TestMonitorLearnwareVerify.monitor_process.kill()
        pass

    def test_add_valid_learnware(self):
        headers = testops.login(TestMonitorLearnwareVerify.email, TestMonitorLearnwareVerify.password)
        learnware_id = testops.add_test_learnware(
            TestMonitorLearnwareVerify.email, TestMonitorLearnwareVerify.password)

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
        testops.delete_learnware(learnware_id, headers)
        pass

    def test_add_invalid_learnware(self):
        headers = testops.login(TestMonitorLearnwareVerify.email, TestMonitorLearnwareVerify.password)
        learnware_id = testops.add_test_learnware(
            TestMonitorLearnwareVerify.email, TestMonitorLearnwareVerify.password,
            learnware_filename='test_learnware_invalid.zip')

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

        self.assertEqual(status, LearnwareVerifyStatus.FAIL.value)
        self.assertTrue(
            os.path.exists(context.get_learnware_verify_file_path(learnware_id)))
        result = testops.url_request(
            'user/list_learnware',
            {'page': 0, 'limit': 10},
            headers=headers
        )

        self.assertEqual(result['code'], 0)
        self.assertEqual(result['data']['total_pages'], 0)
        self.assertEqual(len(result['data']['learnware_list']), 0)
        pass

    def test_add_conda_learnware(self):
        headers = testops.login(TestMonitorLearnwareVerify.email, TestMonitorLearnwareVerify.password)
        learnware_id = testops.add_test_learnware(
            TestMonitorLearnwareVerify.email, TestMonitorLearnwareVerify.password,
            learnware_filename='test_learnware_conda.zip')

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

