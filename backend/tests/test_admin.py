import unittest
from scripts import main
import multiprocessing
from context import config as C
import context
from tests import common_test_operations as testops
import lib.database_operations as dbops
import flask_bcrypt
import hashlib


class TestAdmin(unittest.TestCase):
    def setUpClass() -> None:
        testops.cleanup_folder()
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
        testops.cleanup_folder()
        pass

    def test_list_user(
        self,
    ):
        headers = testops.login("admin@localhost", TestAdmin.password, hash_password=True)
        result = testops.url_request("admin/list_user", {"page": 0, "limit": 10}, headers=headers)

        self.assertEqual(result["code"], 0)
        self.assertEqual(len(result["data"]["user_list"]), 2)

        pass

    def test_delete_user(
        self,
    ):
        headers = testops.login("admin@localhost", TestAdmin.password, hash_password=True)
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
        headers = testops.login("admin@localhost", TestAdmin.password, hash_password=True)
        result = testops.url_request("admin/reset_password", {"id": TestAdmin.user_id}, headers=headers)

        self.assertEqual(result["code"], 0)

        password = result["data"]["password"]
        md5 = result["data"]["md5"]

        result = testops.url_request("auth/login", {"email": "test@localhost", "password": md5})

        self.assertEqual(result["code"], 0)

        origin_admin_pwd = dbops.get_user_info(by="id", value=1)["password"]
        result = testops.url_request("admin/reset_password", {"id": 1}, headers=headers)

        self.assertEqual(result["code"], 0)

        password = result["data"]["md5"]
        result = testops.url_request("auth/login", {"email": "admin@localhost", "password": password})

        dbops.update_user_password(by="email", value="admin@localhost", pwd=origin_admin_pwd)
        self.assertEqual(result["code"], 0)

        pass

    def test_summary(self):
        headers = testops.login("admin@localhost", TestAdmin.password, hash_password=True)
        result = testops.url_request("admin/summary", headers=headers)

        self.assertEqual(result["code"], 0)
        self.assertEqual(result["data"]["count_verified_user"], 2)
        self.assertEqual(result["data"]["count_unverified_user"], 0)
        self.assertEqual(result["data"]["count_verified_learnware"], 1)
        self.assertEqual(result["data"]["count_unverified_learnware"], 0)
        self.assertEqual(result["data"]["count_learnware_awaiting_storage"], 0)
        self.assertEqual(result["data"]["count_download"], 0)
        self.assertGreaterEqual(result["data"]["count_detail"]["Data"]["Table"], 1)
        pass

    def test_list_learnware(self):
        headers = testops.login("admin@localhost", TestAdmin.password, hash_password=True)
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

        headers = testops.login("admin@localhost", TestAdmin.password, hash_password=True)
        result = testops.url_request("admin/delete_learnware", {"learnware_id": learnware_id}, headers=headers)

        self.assertEqual(result["code"], 0)
        pass

    def test_set_user_role(self):
        user_id = testops.url_request(
            "auth/register",
            {"username": "test2", "password": "test", "email": "test2@localhost", "confirm_email": False},
        )["data"]["user_id"]

        super_admin_header = testops.login("admin@localhost", TestAdmin.password, hash_password=True)

        result = testops.url_request("admin/set_user_role", {"user_id": user_id, "role": 1}, headers=super_admin_header)
        self.assertEqual(result["code"], 0)

        user_header = testops.login("test2@localhost", "test")
        result = testops.url_request("admin/list_user", {"page": 0, "limit": 10}, headers=user_header)

        self.assertEqual(result["code"], 0)

        result = testops.url_request("admin/set_user_role", {"user_id": user_id, "role": 1}, headers=user_header)
        self.assertEqual(result["code"], 12)

        testops.url_request("admin/delete_user", {"user_id": user_id}, headers=super_admin_header)
        pass


if __name__ == "__main__":
    unittest.main()
