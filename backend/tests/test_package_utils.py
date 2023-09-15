

import unittest
import multiprocessing
import context
import requests
import os
import shutil
from tests import common_test_operations as testops
import time
import tempfile
from lib import package_utils
import subprocess


class TestPackageUtils(unittest.TestCase):


    def test_pip(self):
        with tempfile.NamedTemporaryFile(suffix=".txt") as ftemp:
            package_utils.filter_nonexist_pip_packages_file('tests/data/requirements.txt', ftemp.name)
            subprocess.check_call(args=['python3', '-m', 'pip', 'install', '-r', ftemp.name])
            pass
        pass

    def test_conda(self):
        with tempfile.NamedTemporaryFile(suffix=".yaml") as ftemp:
            package_utils.filter_nonexist_conda_packages_file('tests/data/env.yaml', ftemp.name)
            try:
                subprocess.check_call(args=['conda', 'env', 'update', '--file', ftemp.name, '--name', 'test_env'])
            finally:
                os.system('conda env remove --name test_env')
                pass
            pass
        pass

if __name__ == '__main__':
    unittest.main()

