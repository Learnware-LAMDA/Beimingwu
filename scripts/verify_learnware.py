import argparse
import learnware.learnware
import learnware.market
import learnware
import json
import shortuuid
import os
import zipfile
import tempfile
from market.backend_martket import BackendMarket



current_module_dir = os.path.dirname(os.path.abspath(__file__))
learnware_backend_package_dir = os.path.join(current_module_dir, '..')
learnware_package_dir = os.path.join(current_module_dir, '..', '..', 'learnware')


def system(command: str):
    retcd = os.system(command)

    if retcd != 0:
        raise RuntimeError(f"Command {command} failed with return code {retcd}")
    
    return retcd


def main(learnware_path, result_file_path):
    learnware_obj = learnware.learnware.get_learnware_from_dirpath('test_id', dict(), learnware_path)

    check_result = BackendMarket.check_learnware(learnware_obj)
    if check_result == BackendMarket.USABLE_LEARWARE:
        result_code = 'SUCCESS'
        pass
    else:
        result_code = 'FAIL'

    result = {
        'result_code': result_code,
    }

    with open(result_file_path, 'w') as f:
        json.dump(result, f)
        pass


def create_env(learnware_path, result_file_path):
    run_id = shortuuid.uuid()
    conda_env = f"learnware_{run_id}"
    extract_path = tempfile.TemporaryDirectory(prefix="learnware_").name

    if not os.path.exists(extract_path):
        os.makedirs(extract_path, exist_ok=True)
        pass

    try:
        print(f"Extracting learnware to {extract_path}")
        with zipfile.ZipFile(learnware_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)
            pass

        if os.path.exists(f"{extract_path}/requirements.txt"):
            print(f'Creating conda env from requirements.txt')
            system(f"conda create -n {conda_env} --clone base")
            system(f"conda run -n {conda_env} python3 -m pip install -r {extract_path}/requirements.txt")
            pass
        elif os.path.exists(f"{extract_path}/environment.yaml"):
            print(f"Creating conda env {conda_env} from {extract_path}/environment.yaml")
            system(f"conda env update --name {conda_env} --file {extract_path}/environment.yaml")
            system(f"conda run -n {conda_env} --no-capture-output python3 -m pip install --upgrade pip")
            print(f"Installing learnware package from {learnware_package_dir}")
            system(f'conda run -n {conda_env} --no-capture-output python3 -m pip install {learnware_package_dir}/')
            system(f'conda run -n {conda_env} --no-capture-output python3 -m pip install -r {learnware_backend_package_dir}/requirements.txt')
            pass
        else:
            raise Exception("No environment.yml or requirements.txt found in learnware")
        
        system(
            f"conda run -n {conda_env} --no-capture-output python3 {__file__} --learnware-path {extract_path} --result-file-path {result_file_path}")
        
    finally:
        system(f"conda env remove -n {conda_env}")
        system('rm -rf ' + extract_path)
        print('finished cleanning up')
        pass
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--learnware-path', type=str, required=True)
    parser.add_argument('--result-file-path', type=str, required=True)
    parser.add_argument('--create-env', action='store_true')

    args = parser.parse_args()

    learnware_path = args.learnware_path
    result_file_path = args.result_file_path
    is_create_env = args.create_env

    if is_create_env:
        create_env(learnware_path, result_file_path)
        pass
    else:
        main(learnware_path, result_file_path)
    pass