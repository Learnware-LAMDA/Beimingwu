import os
import unittest
import json
import tempfile
import zipfile
import common_test_operations as testops


class TestVerifyLearnware(unittest.TestCase):
    def setUp(
        self,
    ) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()
        os.system("rm -rf tests/data/test_result.txt")
        pass

    def test_verify_valid_learnware(self):
        path_learnware = os.path.join("tests", "data", "test_learnware.zip")
        path_result = os.path.join("tests", "data", "test_result.txt")
        semantic_specification = testops.test_learnware_semantic_specification_table()

        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(path_learnware, "r") as zip_ref:
                zip_ref.extractall(temp_dir)
                pass

            semantic_path = os.path.join(temp_dir, "semantic_specification.json")
            with open(semantic_path, "w") as f:
                json.dump(semantic_specification, f)
                pass

            script = os.path.join("scripts", "verify_learnware.py")
            os.system(
                "python3 {3} --learnware-path {0} --semantic-path {1} --result-file-path {2} --create-env".format(
                    temp_dir, semantic_path, path_result, script
                )
            )
            pass

        self.assertTrue(os.path.exists(path_result))
        pass

    def test_verify_invalid_learnware(self):
        path_learnware = os.path.join("tests", "data", "test_learnware_invalid.zip")
        path_result = os.path.join("tests", "data", "test_result.txt")

        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(path_learnware, "r") as zip_ref:
                zip_ref.extractall(temp_dir)
                pass

            semantic_specification = testops.test_learnware_semantic_specification_table()

            semantic_path = os.path.join(temp_dir, "semantic_specification.json")
            with open(semantic_path, "w") as f:
                json.dump(semantic_specification, f)
                pass
            script = os.path.join("scripts", "verify_learnware.py")
            os.system(
                "python3 {3} --learnware-path {0} --semantic-path {1} --result-file-path {2} --create-env".format(
                    temp_dir, semantic_path, path_result, script
                )
            )
            pass

        self.assertTrue(os.path.exists(path_result))

        with open(path_result, "r") as f:
            result = json.load(f)
            pass

        self.assertEqual(result["result_code"], "FAIL")
        pass

    def test_verify_learnware_multi_import_old(self):
        path_learnware = os.path.join("tests", "data", "test_learnware_multi_import_old.zip")
        path_result = os.path.join("tests", "data", "test_result.txt")

        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(path_learnware, "r") as zip_ref:
                zip_ref.extractall(temp_dir)
                pass

            semantic_specification = testops.test_learnware_semantic_specification_table()

            semantic_path = os.path.join(temp_dir, "semantic_specification.json")
            with open(semantic_path, "w") as f:
                json.dump(semantic_specification, f)
                pass
            script = os.path.join("scripts", "verify_learnware.py")
            os.system(
                "python3 {3} --learnware-path {0} --semantic-path {1} --result-file-path {2} --create-env".format(
                    temp_dir, semantic_path, path_result, script
                )
            )
            pass

        self.assertTrue(os.path.exists(path_result))

        with open(path_result, "r") as f:
            result = json.load(f)
            pass

        self.assertEqual(result["result_code"], "FAIL")

        os.remove(path_result)
        pass

    def test_verify_learnware_multi_import(self):
        path_learnware = os.path.join("tests", "data", "test_learnware_multi_import.zip")
        path_result = os.path.join("tests", "data", "test_result.txt")

        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(path_learnware, "r") as zip_ref:
                zip_ref.extractall(temp_dir)
                pass

            semantic_specification = testops.test_learnware_semantic_specification_table()

            semantic_path = os.path.join(temp_dir, "semantic_specification.json")
            with open(semantic_path, "w") as f:
                json.dump(semantic_specification, f)
                pass
            script = os.path.join("scripts", "verify_learnware.py")
            os.system(
                "python3 {3} --learnware-path {0} --semantic-path {1} --result-file-path {2} --create-env".format(
                    temp_dir, semantic_path, path_result, script
                )
            )
            pass

        self.assertTrue(os.path.exists(path_result))

        with open(path_result, "r") as f:
            result = json.load(f)
            pass

        self.assertEqual(result["result_code"], "SUCCESS")

        os.remove(path_result)
        pass


if __name__ == "__main__":
    unittest.main()
