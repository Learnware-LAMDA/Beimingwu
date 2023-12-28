"""this script is executed in k8s pod
"""
import argparse

from learnware.market import EasyStatChecker, BaseChecker
from learnware.learnware import get_learnware_from_dirpath
import os
import json


def verify_learnware(learnware_path, checker_name):
    """verify learnware script"""
    checker = eval(checker_name + "()")
    semantic_path = os.path.join(learnware_path, "semantic_specification.json")
    with open(semantic_path, "r") as f:
        semantic_spec = json.load(f)
        pass
    learnware = get_learnware_from_dirpath("testid", semantic_spec=semantic_spec, learnware_dirpath=learnware_path)

    result, message = checker(learnware)
    # learnware package is not updated
    # if result != BaseChecker.USABLE_LEARNWARE:
    if result != 1:
        raise RuntimeError(message)
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify learnware script")
    parser.add_argument("--learnware_path", type=str, help="learnware path")
    parser.add_argument("--checker_name", type=str, help="checker name")

    args = parser.parse_args()

    verify_learnware(args.learnware_path, args.checker_name)
    pass
