import argparse
import learnware.learnware
import learnware.market
import learnware
import json
import shortuuid
import os
import zipfile
import tempfile
from learnware.market import BaseChecker, EasyStatisticalChecker
from lib import package_utils


current_module_dir = os.path.dirname(os.path.abspath(__file__))
learnware_backend_package_dir = os.path.join(current_module_dir, "..")
learnware_package_dir = os.path.join(current_module_dir, "..", "..", "learnware")


def system(command: str):
    retcd = os.system(command)

    if retcd != 0:
        raise RuntimeError(f"Command {command} failed with return code {retcd}")

    return retcd


def main(learnware_path, semantic_path, result_file_path):
    with open(semantic_path, "r") as f:
        semantic_specification = json.load(f)
        pass

    learnware_obj = learnware.learnware.get_learnware_from_dirpath("test_id", semantic_specification, learnware_path)

    statistic_checker = EasyStatisticalChecker()
    check_result = statistic_checker(learnware_obj)
    if check_result == BaseChecker.USABLE_LEARWARE:
        result_code = "SUCCESS"
        pass
    else:
        result_code = "FAIL"

    result = {
        "result_code": result_code,
    }

    with open(result_file_path, "w") as f:
        json.dump(result, f)
        pass


def create_env(learnware_path, semantic_path, result_file_path):
    run_id = shortuuid.uuid()
    conda_env = f"learnware_{run_id}"
    # extract_path = tempfile.TemporaryDirectory(prefix="learnware_").name
    extract_path = learnware_path

    if not os.path.exists(extract_path):
        os.makedirs(extract_path, exist_ok=True)
        pass

    try:
        if os.path.exists(f"{extract_path}/requirements.txt"):
            print(f"Creating conda env from requirements.txt")
            system(f"conda create -n {conda_env} --clone base")
            system(f"conda run -n {conda_env} python3 -m pip install --force-reinstall werkzeug")

            with tempfile.NamedTemporaryFile(prefix="verify_pip_", suffix=".txt") as ftemp:
                package_utils.filter_nonexist_pip_packages_file(f"{extract_path}/requirements.txt", ftemp.name)
                system(f"conda run -n {conda_env} python3 -m pip install -r {ftemp.name}")
                pass
            pass

        elif os.path.exists(f"{extract_path}/environment.yaml"):
            print(f"Creating conda env {conda_env} from {extract_path}/environment.yaml")
            with tempfile.NamedTemporaryFile(prefix="verify_conda_", suffix=".yaml") as ftemp:
                package_utils.filter_nonexist_conda_packages_file(f"{extract_path}/environment.yaml", ftemp.name)
                system(f"conda env update --name {conda_env} --file {ftemp.name}")
                pass

            system(f"conda run -n {conda_env} --no-capture-output python3 -m pip install --upgrade pip")
            print(f"Installing learnware package from {learnware_package_dir}")
            system(f"conda run -n {conda_env} --no-capture-output python3 -m pip install {learnware_package_dir}/")
            system(
                f"conda run -n {conda_env} --no-capture-output python3 -m pip install -r {learnware_backend_package_dir}/requirements.txt"
            )
            pass
        else:
            raise Exception("No environment.yml or requirements.txt found in learnware")

        system(
            (
                f"conda run -n {conda_env} --no-capture-output python3 {__file__} --learnware-path {extract_path}"
                f" --semantic-path {semantic_path} --result-file-path {result_file_path}"
            )
        )

    finally:
        system(f"conda env remove -n {conda_env}")
        print("finished cleanning up")
        pass
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--learnware-path", type=str, required=True)
    parser.add_argument("--semantic-path", type=str, required=True)
    parser.add_argument("--result-file-path", type=str, required=True)
    parser.add_argument("--create-env", action="store_true")

    args = parser.parse_args()

    learnware_path = args.learnware_path
    semantic_path = args.semantic_path
    result_file_path = args.result_file_path
    is_create_env = args.create_env

    if is_create_env:
        create_env(learnware_path, semantic_path, result_file_path)
        pass
    else:
        main(learnware_path, semantic_path, result_file_path)
    pass
