import os
import unittest
import json


class TestVerifyLearnware(unittest.TestCase):

    def setUp(self,) -> None:
        super().setUp()


    def tearDown(self) -> None:
        super().tearDown()
        os.system('rm -rf tests/data/test_result.txt')
        pass

    def test_verify_valid_learnware(self):
        path_learnware = os.path.join('tests', 'data', 'test_learnware_pip.zip')
        path_result = os.path.join('tests', 'data', 'test_result.txt')

        script = os.path.join('exec', 'verify_learnware.py')
        os.system('python3 {2} --learnware-path {0} --result-file-path {1} --create-env'.format(
            path_learnware, path_result, script))

        self.assertTrue(os.path.exists(path_result))
        pass

    def test_verify_invalid_learnware(self):
        path_learnware = os.path.join('tests', 'data', 'test_learnware_invalid.zip')
        path_result = os.path.join('tests', 'data', 'test_result.txt')

        script = os.path.join('exec', 'verify_learnware.py')
        os.system('python3 {2} --learnware-path {0} --result-file-path {1} --create-env'.format(
            path_learnware, path_result, script))

        self.assertTrue(os.path.exists(path_result))

        with open(path_result, 'r') as f:
            result = json.load(f)
            pass

        self.assertEqual(result['result_code'], 'FAIL')
        pass


if __name__ == '__main__':
    unittest.main()

