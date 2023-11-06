import unittest
from scripts import main
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
import datetime


class TestUser(unittest.TestCase):
    def setUpClass() -> None:
        testops.cleanup_folder()
        unittest.TestCase.setUpClass()
        TestUser.server_process = multiprocessing.Process(target=main.main)
        TestUser.server_process.start()
        testops.wait_port_open(context.config.listen_port, 10)
        context.init_database()
        testops.clear_db()
        TestUser.username = "test"
        TestUser.email = "test@localhost"
        TestUser.password = "test"
        testops.url_request(
            "auth/register",
            {
                "username": TestUser.username,
                "password": TestUser.password,
                "email": TestUser.email,
                "confirm_email": False,
            },
        )

    def tearDownClass() -> None:
        unittest.TestCase.tearDownClass()
        TestUser.server_process.kill()
        testops.cleanup_folder()
        pass

    def test_profile(self):
        headers = testops.login(TestUser.email, TestUser.password)
        result = testops.url_request("user/profile", {}, headers=headers)

        self.assertEqual(result["code"], 0)
        self.assertEqual(result["data"]["username"], TestUser.username)
        pass

    def test_change_password(self):
        headers = testops.login(TestUser.email, TestUser.password)
        result = testops.url_request(
            "user/change_password", {"old_password": TestUser.password, "new_password": "test2"}, headers=headers
        )

        self.assertEqual(result["code"], 0)

        result = testops.url_request("auth/logout", {}, headers=headers)

        self.assertEqual(result["code"], 0)

        headers = testops.login(TestUser.email, "test2")

        result = testops.url_request(
            "user/change_password", {"old_password": "test2", "new_password": TestUser.password}, headers=headers
        )

        self.assertEqual(result["code"], 0)

        pass

    def test_list_learnware(self):
        headers = testops.login(TestUser.email, TestUser.password)
        semantic_specification = testops.test_learnware_semantic_specification()

        learnware_file = open(os.path.join("tests", "data", "test_learnware.zip"), "rb")
        files = {"learnware_file": learnware_file}

        # print(semantic_specification)
        result = testops.url_request(
            "user/add_learnware",
            {"semantic_specification": json.dumps(semantic_specification)},
            files=files,
            headers=headers,
        )

        learnware_file.close()
        self.assertEqual(result["code"], 0)
        learnware_id = result["data"]["learnware_id"]

        self.assertTrue(os.path.exists(context.get_learnware_verify_file_path(learnware_id)))

        result = testops.url_request("user/list_learnware", {"page": 0, "limit": 10}, headers=headers)

        self.assertEqual(result["code"], 0)
        self.assertEqual(result["data"]["total_pages"], 1)
        self.assertEqual(result["data"]["learnware_list"][0]["learnware_id"], learnware_id)

        testops.add_learnware_to_engine(learnware_id, headers)

        result = testops.url_request("user/list_learnware", {"page": 0, "limit": 10}, headers=headers)

        self.assertEqual(result["code"], 0)
        self.assertEqual(result["data"]["total_pages"], 1)
        self.assertEqual(result["data"]["learnware_list"][0]["learnware_id"], learnware_id)

        result = testops.url_request("user/delete_learnware", {"learnware_id": learnware_id}, headers=headers)

        self.assertEqual(result["code"], 0)

        result = testops.url_request(
            "user/list_learnware", {"page": 0, "limit": 10, "is_verified": False}, headers=headers
        )

        self.assertEqual(result["code"], 0)
        self.assertEqual(len(result["data"]["learnware_list"]), 0)

        pass

    def test_add_learnware(self):
        headers = testops.login(TestUser.email, TestUser.password)
        semantic_specification = testops.test_learnware_semantic_specification()

        learnware_file = open(os.path.join("tests", "data", "test_learnware.zip"), "rb")
        files = {"learnware_file": learnware_file}

        # print(semantic_specification)
        result = testops.url_request(
            "user/add_learnware",
            {"semantic_specification": json.dumps(semantic_specification)},
            files=files,
            headers=headers,
        )

        learnware_file.close()
        self.assertEqual(result["code"], 0)
        learnware_id = result["data"]["learnware_id"]
        learnware_info, _ = dbops.get_learnware_list(by="learnware_id", value=learnware_id)
        learnware_info = learnware_info[0]
        self.assertEqual(learnware_info["verify_status"], "WAITING")

        testops.delete_learnware(learnware_id, headers)
        pass

    def test_add_folder_learnware(self):
        headers = testops.login(TestUser.email, TestUser.password)
        semantic_specification = testops.test_learnware_semantic_specification()

        learnware_file = open(os.path.join("tests", "data", "test_learnware_folder.zip"), "rb")
        files = {"learnware_file": learnware_file}

        # print(semantic_specification)
        result = testops.url_request(
            "user/add_learnware",
            {"semantic_specification": json.dumps(semantic_specification)},
            files=files,
            headers=headers,
        )

        learnware_file.close()
        self.assertEqual(result["code"], 0)
        learnware_id = result["data"]["learnware_id"]
        learnware_info, _ = dbops.get_learnware_list(by="learnware_id", value=learnware_id)
        learnware_info = learnware_info[0]
        self.assertEqual(learnware_info["verify_status"], "WAITING")

        testops.delete_learnware(learnware_id, headers)
        pass

    def test_update_unverified_learnware(self):
        headers = testops.login(TestUser.email, TestUser.password)
        semantic_specification = testops.test_learnware_semantic_specification()

        learnware_file = open(os.path.join("tests", "data", "test_learnware.zip"), "rb")
        files = {"learnware_file": learnware_file}

        # print(semantic_specification)
        result = testops.url_request(
            "user/add_learnware",
            {"semantic_specification": json.dumps(semantic_specification)},
            files=files,
            headers=headers,
        )

        learnware_file.close()
        self.assertEqual(result["code"], 0)
        learnware_id = result["data"]["learnware_id"]

        result = testops.url_request("user/list_learnware", {"page": 0, "limit": 10}, headers=headers)

        self.assertEqual(result["code"], 0)
        learnware_info = result["data"]["learnware_list"][0]
        print(learnware_info.keys())
        self.assertEqual(learnware_info["semantic_specification"]["Name"]["Values"], "Test Classification")

        semantic_specification["Name"]["Values"] = "Test Classification 2"
        dbops.update_learnware_timestamp(learnware_id, timestamp=(datetime.datetime.now() - datetime.timedelta(days=1)))
        result = testops.url_request(
            "user/update_learnware",
            data={"learnware_id": learnware_id, "semantic_specification": json.dumps(semantic_specification)},
            headers=headers,
        )

        self.assertEqual(result["code"], 0)

        result = testops.url_request("user/list_learnware", {"page": 0, "limit": 10}, headers=headers)

        self.assertEqual(result["code"], 0)
        learnware_info = result["data"]["learnware_list"][0]
        self.assertEqual(learnware_info["semantic_specification"]["Name"]["Values"], "Test Classification 2")
        print("---------------" + learnware_info["last_modify"])
        last_modify = datetime.datetime.strptime(learnware_info["last_modify"], "%Y-%m-%d %H:%M:%S.%f %Z")
        self.assertTrue((datetime.datetime.now() - last_modify).total_seconds() < 10)

        testops.delete_learnware(learnware_id, headers)
        pass

    def test_update_verified_learnware(self):
        headers = testops.login(TestUser.email, TestUser.password)

        learnware_id = testops.add_test_learnware(TestUser.email, TestUser.password)

        result = testops.url_request("user/list_learnware", {"page": 0, "limit": 10}, headers=headers)

        self.assertEqual(result["code"], 0)
        learnware_info = result["data"]["learnware_list"][0]
        self.assertEqual(learnware_info["semantic_specification"]["Name"]["Values"], "Test Classification")

        semantic_specification = learnware_info["semantic_specification"]

        semantic_specification["Name"]["Values"] = "Test Classification 2"
        result = testops.url_request(
            "user/update_learnware",
            data={"learnware_id": learnware_id, "semantic_specification": json.dumps(semantic_specification)},
            headers=headers,
        )

        self.assertEqual(result["code"], 0)
        result = testops.url_request(
            "user/list_learnware", {"page": 0, "limit": 10, "is_verified": False}, headers=headers
        )

        self.assertEqual(result["code"], 0)
        learnware_info = result["data"]["learnware_list"][0]
        self.assertEqual(learnware_info["semantic_specification"]["Name"]["Values"], "Test Classification 2")
        assert learnware_info["verify_status"] != "SUCCESS"

        testops.delete_learnware(learnware_id, headers)
        pass

    def test_update_verified_learnware_and_file(self):
        headers = testops.login(TestUser.email, TestUser.password)
        semantic_specification = testops.test_learnware_semantic_specification()

        learnware_file = open(os.path.join("tests", "data", "test_learnware.zip"), "rb")
        files = {"learnware_file": learnware_file}

        # print(semantic_specification)
        result = testops.url_request(
            "user/add_learnware",
            {"semantic_specification": json.dumps(semantic_specification)},
            files=files,
            headers=headers,
        )

        learnware_file.close()
        self.assertEqual(result["code"], 0)
        learnware_id = result["data"]["learnware_id"]

        testops.add_learnware_to_engine(learnware_id, headers)

        response = testops.url_request(
            "engine/download_learnware",
            {"learnware_id": learnware_id},
            headers=headers,
            method="get",
            return_response=True,
        )

        self.assertEqual(len(response.content), os.path.getsize(os.path.join("tests", "data", "test_learnware.zip")))

        learnware_file = open(os.path.join("tests", "data", "test_learnware2.zip"), "rb")
        files = {"learnware_file": learnware_file}

        result = testops.url_request(
            "user/update_learnware",
            data={"learnware_id": learnware_id, "semantic_specification": json.dumps(semantic_specification)},
            files=files,
            headers=headers,
        )
        learnware_file.close()

        result = testops.url_request("user/list_learnware", {"page": 0, "limit": 10}, headers=headers)

        self.assertEqual(result["code"], 0)
        learnware_info = result["data"]["learnware_list"][0]
        self.assertEqual(learnware_info["verify_status"], "WAITING")
        self.assertTrue(os.path.exists(context.get_learnware_verify_file_path(learnware_id)))

        response = testops.url_request(
            "engine/download_learnware",
            {"learnware_id": learnware_id},
            headers=headers,
            method="get",
            return_response=True,
        )

        self.assertEqual(len(response.content), os.path.getsize(os.path.join("tests", "data", "test_learnware2.zip")))

        testops.delete_learnware(learnware_id, headers)
        pass

    def test_verify_log(self):
        learnware_id = testops.add_test_learnware(TestUser.email, TestUser.password)
        dbops.update_learnware_verify_result(learnware_id, LearnwareVerifyStatus.SUCCESS, "test result")
        headers = testops.login(TestUser.email, TestUser.password)

        result = testops.url_request(
            "user/verify_log?learnware_id={}".format(learnware_id),
            {},
            headers=headers,
            method="get",
            return_response=True,
        )

        result = result.json()["data"]

        self.assertEqual(result, "test result")
        testops.delete_learnware(learnware_id, headers)
        pass

    def test_verify_log_by_admin(self):
        learnware_id = testops.add_test_learnware(TestUser.email, TestUser.password)
        dbops.update_learnware_verify_result(learnware_id, LearnwareVerifyStatus.SUCCESS, "test result")
        headers = testops.login("test@localhost", "test")

        result = testops.url_request(
            "user/verify_log?learnware_id={}".format(learnware_id),
            {},
            headers=headers,
            method="get",
            return_response=True,
        )

        result = result.json()["data"]

        self.assertEqual(result, "test result")
        testops.delete_learnware(learnware_id, headers)
        pass

    def test_add_learnware_no_stat_file(self):
        headers = testops.login(TestUser.email, TestUser.password)
        semantic_specification = testops.test_learnware_semantic_specification()

        learnware_file = open(os.path.join("tests", "data", "test_learnware_no_stat.zip"), "rb")
        files = {"learnware_file": learnware_file}

        # print(semantic_specification)
        result = testops.url_request(
            "user/add_learnware",
            {"semantic_specification": json.dumps(semantic_specification)},
            files=files,
            headers=headers,
        )

        learnware_file.close()
        self.assertEqual(result["code"], 51)

        pass

    def test_create_token(self):
        headers = testops.login(TestUser.email, TestUser.password)

        result = testops.url_request("user/create_token", {}, headers=headers)

        self.assertEqual(result["code"], 0)

        token = result["data"]["token"]

        result = testops.url_request("user/list_token", {}, headers=headers)

        self.assertEqual(result["code"], 0)
        self.assertIn(token, result["data"]["token_list"])

        result = testops.url_request("user/delete_token", {"token": token}, headers=headers)

        self.assertEqual(result["code"], 0)

        result = testops.url_request("user/list_token", {}, headers=headers)

        print(result)
        self.assertEqual(result["code"], 0)
        self.assertEqual(len(result["data"]["token_list"]), 0)
        pass


if __name__ == "__main__":
    unittest.main()
