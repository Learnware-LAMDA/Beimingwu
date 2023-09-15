import unittest
from scripts import main
import multiprocessing
from context import config as C
import context
from tests import common_test_operations as testops
import lib.database_operations as dbops
import flask_bcrypt


class TestAdmin(unittest.TestCase):
    def setUpClass() -> None:
        unittest.TestCase.setUpClass()
        TestAdmin.server_process = multiprocessing.Process(target=main.main)
        TestAdmin.server_process.start()
        testops.wait_port_open(C.listen_port, 10)
        context.init_database()
        testops.clear_db()
        TestAdmin.user_id = testops.url_request(
            "auth/register", {"username": "test", "password": "test", "email": "test@localhost", "confirm_email": False}
        )["data"]["user_id"]
        TestAdmin.learnware_id = testops.add_test_learnware("test@localhost", "test")
        TestAdmin.password = "admin"

    def tearDownClass() -> None:
        unittest.TestCase.tearDownClass()
        TestAdmin.server_process.kill()
        pass

    def test_list_user(
        self,
    ):
        headers = testops.login("admin@localhost", TestAdmin.password)
        result = testops.url_request("admin/list_user", {"page": 0, "limit": 10}, headers=headers)

        self.assertEqual(result["code"], 0)
        self.assertEqual(len(result["data"]["user_list"]), 2)

        pass

    def test_delete_user(
        self,
    ):
        headers = testops.login("admin@localhost", TestAdmin.password)
        result = testops.url_request(
            "admin/delete_learnware", {"learnware_id": TestAdmin.learnware_id}, headers=headers
        )

        self.assertEqual(result["code"], 0)

        result = testops.url_request("admin/delete_user", {"user_id": TestAdmin.user_id}, headers=headers)

        self.assertEqual(result["code"], 0)

        result = testops.url_request("admin/list_user", {"page": 0, "limit": 10}, headers=headers)

        self.assertEqual(result["code"], 0)
        self.assertEqual(result["data"]["user_list"][0]["username"], "admin")
        self.assertEqual(len(result["data"]["user_list"]), 1)

        testops.url_request(
            "auth/register", {"username": "test", "password": "test", "email": "test@localhost", "confirm_email": False}
        )

        TestAdmin.learnware_id = testops.add_test_learnware("test@localhost", "test")

        pass

    def test_reset_password(self):
        headers = testops.login("admin@localhost", TestAdmin.password)
        result = testops.url_request("admin/reset_password", {"id": TestAdmin.user_id}, headers=headers)

        self.assertEqual(result["code"], 0)

        password = result["data"]["password"]
        md5 = result["data"]["md5"]

        result = testops.url_request("auth/login", {"email": "test@localhost", "password": md5})

        self.assertEqual(result["code"], 0)

        result = testops.url_request("admin/reset_password", {"id": 1}, headers=headers)

        self.assertEqual(result["code"], 0)

        password = result["data"]["password"]
        result = testops.url_request("auth/login", {"email": "admin@localhost", "password": password})

        self.assertEqual(result["code"], 0)

        dbops.update_user_password(
            "email", "admin@localhost", flask_bcrypt.generate_password_hash("admin").decode("utf-8")
        )
        pass

    def test_summary(self):
        headers = testops.login("admin@localhost", TestAdmin.password)
        result = testops.url_request("admin/summary", headers=headers)

        self.assertEqual(result["code"], 0)
        self.assertEqual(result["data"]["count_user"], 2)
        self.assertEqual(result["data"]["count_verified_learnware"], 1)
        self.assertEqual(result["data"]["count_unverified_learnware"], 0)
        self.assertEqual(result["data"]["count_download"], 0)
        self.assertGreaterEqual(result["data"]["count_detail"]["Data"]["Image"], 1)
        pass

    def test_list_learnware(self):
        headers = testops.login("admin@localhost", TestAdmin.password)
        result = testops.url_request("admin/list_learnware", {"page": 0, "limit": 10}, headers=headers)

        self.assertEqual(result["code"], 0)
        self.assertGreaterEqual(len(result["data"]["learnware_list_single"]), 1)

        result = testops.url_request(
            "admin/list_learnware", {"page": 0, "limit": 10, "is_verified": True}, headers=headers
        )

        self.assertEqual(result["code"], 0)
        self.assertGreaterEqual(len(result["data"]["learnware_list_single"]), 1)

        result = testops.url_request(
            "admin/list_learnware",
            {"page": 0, "limit": 10, "is_verified": True, "user_id": TestAdmin.user_id},
            headers=headers,
        )

        self.assertEqual(result["code"], 0)
        self.assertGreaterEqual(len(result["data"]["learnware_list_single"]), 1)
        pass

    def test_delete_learnware(self):
        learnware_id = testops.add_test_learnware_unverified("test@localhost", "test")

        headers = testops.login("admin@localhost", TestAdmin.password)
        result = testops.url_request("admin/delete_learnware", {"learnware_id": learnware_id}, headers=headers)

        self.assertEqual(result["code"], 0)
        pass


if __name__ == "__main__":
    unittest.main()
