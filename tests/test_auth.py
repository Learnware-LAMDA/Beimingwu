
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


class TestAuth(unittest.TestCase):

    def setUpClass() -> None:
        unittest.TestCase.setUpClass()
        TestAuth.server_process = multiprocessing.Process(target=main.main)
        TestAuth.server_process.start()
        testops.wait_port_open(C.listen_port, 10)
        context.init_database()
        testops.clear_db()

    def tearDownClass() -> None:
        unittest.TestCase.tearDownClass()
        TestAuth.server_process.kill()

    def test_01_login(self):
        # first we need register a user
        result = testops.url_request(
            'auth/register', 
            {'username': 'test', 'password': 'test', "email": "test@localhost", "confirm_email": False})

        self.assertEqual(result['code'], 0)

        # then we need login
        result = testops.url_request(
            'auth/login',
            {'email': 'test@localhost', 'password': 'test'})
        
        self.assertEqual(result['code'], 0)

        token = result['data']['token']
        headers = {'Authorization': f'Bearer {token}'}

        result = testops.url_request(
            'auth/get_role',
            {},
            headers=headers)
        
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['data']['role'], 0)
        
        result = testops.url_request(
            'auth/logout',
            {},
            headers=headers)
        
        self.assertEqual(result['code'], 0)

        # logout

        pass

    def test_02_login_by_token(self):

        result = testops.url_request(
            'auth/login',
            {'email': 'test@localhost', 'password': 'test', 'confirm_email': False})
        

        token = result['data']['token']
        headers = {'Authorization': f'Bearer {token}'}

        result = testops.url_request(
            'user/create_token',
            {},
            headers=headers)
        
        token = result['data']['token']

        testops.url_request(
            'auth/logout',
            {},
            headers=headers)
        
        result = testops.url_request(
            'auth/login_by_token',
            {'email': 'test@localhost', 'token': token})
        
        self.assertEqual(result['code'], 0)
        self.assertIsNotNone(result['data']['token'])

        pass

    def test_login_required(self):
        response = testops.url_request(
            'auth/logout',
            {}, return_response=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], 11)
        pass

    def test_register_by_email(self):
        result = testops.url_request(
            'auth/register', 
            {'username': 'test2', 'password': 'test', "email": "xiaochuan.zou@polixir.ai"})

        self.assertEqual(result['code'], 0)

        # then we need login
        result = testops.url_request(
            'auth/login',
            {'email': 'xiaochuan.zou@polixir.ai', 'password': 'test'})
        
        self.assertEqual(result['code'], 54)

        verify_code = utils.generate_email_verification_code(
            'xiaochuan.zou@polixir.ai', secret_key=context.config["app_secret_key"])
        url = f'auth/email_confirm?code={verify_code}'

        result = testops.url_request(
            url,
            {},)
        
        self.assertEqual(result['code'], 0)
        result = testops.url_request(
            'auth/login',
            {'email': 'xiaochuan.zou@polixir.ai', 'password': 'test'})
        
        self.assertEqual(result['code'], 0)

        self.assertGreater(len(result['data']['token']), 0)

        pass

if __name__ == '__main__':
    unittest.main()

