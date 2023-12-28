import os
import context
import unittest
import multiprocessing
from scripts import main
from context import config as C
import tempfile
import zipfile
import common_test_operations as testops
from learnware.config import C as learnware_config
from learnware.client.utils import install_environment, system_execute
from lib import engine as engine_utils
from scripts.monitor_learnware_verify import verify_learnware_with_conda_checker
import shortuuid


class TestVerifyLearnware(unittest.TestCase):
    def setUpClass() -> None:
        pass

    def tearDownClass() -> None:
        pass

    def test_verify_valid_learnware(self):
        learnware_path = os.path.join("tests", "data", "test_learnware.zip")
        semantic_spec = testops.test_learnware_semantic_specification_table()
        learnware_id = "testid"

        with tempfile.TemporaryDirectory() as learnware_folder:
            engine_utils.repack_learnware_folder(learnware_path, learnware_folder, learnware_id, semantic_spec)
            env_path = str(shortuuid.uuid())
            env_path = os.path.join(context.config["env_path"], env_path)
            install_environment(learnware_folder, None, conda_prefix=env_path)
            system_execute(
                args=[
                    "conda",
                    "run",
                    "--prefix",
                    env_path,
                    "--no-capture-output",
                    "python",
                    "-m",
                    "pip",
                    "install",
                    "torch",
                ]
            )
            retcd = os.system(
                f"conda run --prefix {env_path} --no-capture-output python3 scripts/verify_learnware_script.py --learnware_path {learnware_folder} --checker_name EasyStatChecker"
            )
            os.system(f"conda env remove --prefix {env_path}")

        self.assertEqual(retcd, 0)

        pass

    def test_verify_invalid_learnware(self):
        learnware_path = os.path.join("tests", "data", "test_learnware_invalid.zip")
        semantic_spec = testops.test_learnware_semantic_specification_table()
        learnware_id = "testid"

        with tempfile.TemporaryDirectory() as learnware_folder:
            engine_utils.repack_learnware_folder(learnware_path, learnware_folder, learnware_id, semantic_spec)
            env_path = str(shortuuid.uuid())
            env_path = os.path.join(context.config["env_path"], env_path)
            install_environment(learnware_folder, None, conda_prefix=env_path)
            system_execute(
                args=[
                    "conda",
                    "run",
                    "--prefix",
                    env_path,
                    "--no-capture-output",
                    "python",
                    "-m",
                    "pip",
                    "install",
                    "torch",
                ]
            )
            retcd = os.system(
                f"conda run --prefix {env_path} --no-capture-output python3 scripts/verify_learnware_script.py --learnware_path {learnware_folder} --checker_name EasyStatChecker"
            )
            os.system(f"conda env remove --prefix {env_path}")

        self.assertNotEqual(retcd, 0)
        pass


if __name__ == "__main__":
    unittest.main()
