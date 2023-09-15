import os
import unittest
import json
import lib.command_executor as command_executor
import time


class TestCommandExecutor(unittest.TestCase):
    def setUp(
        self,
    ) -> None:
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()
        pass

    def test_execute_shell(self):
        command = 'echo "hello world"'
        output = command_executor.execute_shell(command)
        self.assertEqual(output, "hello world\n")
        pass

    def test_execute_shell_timeout(self):
        command = 'echo "hello" && sleep 10 && ls /dfadf'
        start = time.time()
        output = command_executor.execute_shell(command, timeout=1)
        end = time.time()
        self.assertLess(end - start, 2)
        print(output)
        pass

    def test_execute_shell_fail(self):
        command = "ls /dafasdfadsfas"
        output = command_executor.execute_shell(command)
        print(output)
        pass


if __name__ == "__main__":
    unittest.main()
