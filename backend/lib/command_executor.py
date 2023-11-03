import os
import zipfile
import subprocess


def execute_shell(command: str, timeout=None, check=False):
    if timeout is not None:
        command = 'timeout {0} sh -c "{1}"'.format(timeout, command.replace('"', '\\"'))
        pass

    result = subprocess.run(
        command, shell=True, stderr=subprocess.STDOUT, check=check, stdout=subprocess.PIPE, env=os.environ.copy()
    )

    return result.stdout.decode("utf-8")
