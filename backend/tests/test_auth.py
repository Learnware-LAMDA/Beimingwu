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


class TestAuth(unittest.TestCase):
    def setUpClass() -> None:
        testops.cleanup_folder()
        unittest.TestCase.setUpClass()
        testops.set_config("register_email_patterns", [".edu.", ".edu"])
        TestAuth.server_process = multiprocessing.Process(target=main.main)
        TestAuth.server_process.start()
        testops.wait_port_open(C.listen_port, 10)
        context.init_database()
        testops.clear_db()

    def tearDownClass() -> None:
        unittest.TestCase.tearDownClass()
        TestAuth.server_process.kill()
        testops.cleanup_folder()
        testops.reset_config()

    def test_01_login(self):
        # first we need register a user
        result = testops.url_request(
            "auth/register",
            {"username": "test", "password": "test", "email": "test@localhost.edu", "confirm_email": False},
        )

        self.assertEqual(result["code"], 0)

        # then we need login
        result = testops.url_request("auth/login", {"email": "test@localhost.edu", "password": "test"})

        self.assertEqual(result["code"], 0)

        token = result["data"]["token"]
        headers = {"Authorization": f"Bearer {token}"}

        result = testops.url_request("auth/get_role", {}, headers=headers)

        self.assertEqual(result["code"], 0)
        self.assertEqual(result["data"]["role"], 0)

        result = testops.url_request("auth/logout", {}, headers=headers)

        self.assertEqual(result["code"], 0)

        pass

    def test_02_login_by_token(self):
        result = testops.url_request(
            "auth/login", {"email": "test@localhost.edu", "password": "test", "confirm_email": False}
        )

        token = result["data"]["token"]
        headers = {"Authorization": f"Bearer {token}"}

        result = testops.url_request("user/create_token", {}, headers=headers)

        token = result["data"]["token"]

        testops.url_request("auth/logout", {}, headers=headers)

        result = testops.url_request("auth/login_by_token", {"email": "test@localhost.edu", "token": token})

        self.assertEqual(result["code"], 0)
        self.assertIsNotNone(result["data"]["token"])

        testops.delete_user_by_email("test@localhost.edu")
        pass

    def test_login_required(self):
        response = testops.url_request("auth/logout", {}, return_response=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["code"], 11)
        pass

    def test_register_by_email(self):
        result = testops.url_request(
            "auth/register", {"username": "test2", "password": "test", "email": "xiaochuan.zou@polixir.edu.ai"}
        )

        self.assertEqual(result["code"], 0)

        time.sleep(5)

        # then we need login
        result = testops.url_request("auth/login", {"email": "xiaochuan.zou@polixir.edu.ai", "password": "test"})

        self.assertEqual(result["code"], 54)

        verify_code = utils.generate_email_verification_code(
            "xiaochuan.zou@polixir.edu.ai", secret_key=context.config["app_secret_key"]
        )
        url = f"auth/email_confirm?code={verify_code}"

        result = testops.url_request(
            url,
            {},
        )

        self.assertEqual(result["code"], 0)
        result = testops.url_request("auth/login", {"email": "xiaochuan.zou@polixir.edu.ai", "password": "test"})

        self.assertEqual(result["code"], 0)

        self.assertGreater(len(result["data"]["token"]), 0)

        testops.delete_user_by_email("xiaochuan.zou@polixir.edu.ai")
        pass

    def test_reset_password(self):
        email = "xiaochuan.zou@polixir.edu.ai"
        result = testops.url_request(
            "auth/register", {"username": "test3", "password": "test", "email": email, "confirm_email": False}
        )
        self.assertEqual(result["code"], 0)
        user_id = result["data"]["user_id"]
        result = testops.url_request("auth/send_reset_password_email", {"email": email})
        self.assertEqual(result["code"], 0)

        time.sleep(5)

        code = utils.generate_email_verification_code(email, secret_key=context.config["app_secret_key"])
        result = testops.url_request("auth/reset_password", {"code": code, "user_id": user_id})
        self.assertEqual(result["code"], 0)
        password_new = result["data"]["password"]

        print(password_new)
        password_hash = hashlib.md5(password_new.encode("utf-8")).hexdigest()
        result = testops.url_request("auth/login", {"email": email, "password": password_hash})
        self.assertEqual(result["code"], 0)
        testops.delete_user_by_email(email)
        pass

    def test_register_not_edu(self):
        result = testops.url_request(
            "auth/register", {"username": "test2", "password": "test", "email": "xiaochuan.zou@polixir.ai"}
        )

        self.assertEqual(result["code"], 41)
        pass


if __name__ == "__main__":
    unittest.main()
