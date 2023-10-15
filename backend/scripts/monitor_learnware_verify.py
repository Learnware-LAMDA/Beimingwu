import time
import context
import lib.database_operations as dbops
import lib.common_utils as common_utils
import queue
import multiprocessing.dummy as mp
import argparse
import os
import lib.command_executor as command_executor
from database.base import LearnwareVerifyStatus
import json
import lib.restful_wrapper as restful_wrapper
import tempfile
import zipfile
import lib.engine as engine_ops
import yaml
import shutil
from typing import Tuple


def verify_learnware_by_script(
    learnware_id: str, learnware_path: str, semantic_spec_filename: str, process_result_filename: str
) -> Tuple[bool, str]:

    verify_script = os.path.join("scripts", "verify_learnware.py")
    verify_command = (
        f"python3 {verify_script} --learnware-path {learnware_path}"
        f" --semantic-path {semantic_spec_filename}"
        f" --result-file-path {process_result_filename} --create-env"
    )

    try:
        command_output = command_executor.execute_shell(verify_command, timeout=context.config.verify_timeout)
    except Exception as e:
        context.logger.exception(e)
        command_output = str(e)
        pass

    verify_sucess = True

    if not os.path.exists(process_result_filename):
        verify_sucess = False
        pass
    else:
        try:
            with open(process_result_filename, "r") as f:
                verify_result = json.load(f)
                pass

            if verify_result["result_code"] != "SUCCESS":
                verify_sucess = False
                pass
        except Exception:
            verify_sucess = False
            pass
        os.remove(process_result_filename)
        pass

    return verify_sucess, command_output


def update_learnware_yaml_file(learnware_path, learnware_id, semantic_spec_filename):
    yaml_file = engine_ops.learnware_config.learnware_folder_config["yaml_file"]
    yaml_file_path = os.path.join(learnware_path, yaml_file)
    with open(yaml_file_path, "r") as f:
        learnware_info = yaml.safe_load(f)
        pass

    shutil.copyfile(semantic_spec_filename, os.path.join(learnware_path, "semantic_specification.json"))
    learnware_info["id"] = learnware_id
    learnware_info["semantic_specification"] = {"file_name": "semantic_specification.json"}
    with open(yaml_file_path, "w") as f:
        yaml.dump(learnware_info, f)
        pass
    pass


def worker_process_func(q: queue.Queue, env: dict):
    if env is not None:
        os.environ.update(env)
        pass

    while True:
        learnware_id = q.get()
        context.logger.info(f"Start to verify learnware: {learnware_id}")

        if not dbops.check_learnware_exist(learnware_id=learnware_id):
            context.logger.info(f"learnware is deleted, no need to process: {learnware_id}")
            continue
            pass

        dbops.update_learnware_verify_status(learnware_id, LearnwareVerifyStatus.PROCESSING)
        learnware_filename = context.get_learnware_verify_file_path(learnware_id)
        semantic_spec_filename = learnware_filename[:-4] + ".json"
        process_result_filename = learnware_filename + ".result"
        learnware_processed_filename = learnware_filename[:-4] + "_processed.zip"

        with tempfile.TemporaryDirectory() as tmpdir:
            extract_path = tmpdir
            if not os.path.exists(extract_path):
                os.makedirs(extract_path)
                pass

            context.logger.info(f"Extracting learnware to {extract_path}")
            with zipfile.ZipFile(learnware_filename, "r") as zip_ref:
                top_folder = common_utils.get_top_folder_in_zip(zip_ref)
                zip_ref.extractall(extract_path)
                pass

            extract_path = os.path.join(extract_path, top_folder)
            update_learnware_yaml_file(extract_path, learnware_id, semantic_spec_filename)

            verify_success, command_output = verify_learnware_by_script(
                learnware_id, extract_path, semantic_spec_filename, process_result_filename
            )

            # the learnware my be deleted
            if not dbops.check_learnware_exist(learnware_id=learnware_id):
                context.logger.info(f"learnware is deleted, no need to process: {learnware_id}")
                continue

            if verify_success:
                verify_status = LearnwareVerifyStatus.SUCCESS
            else:
                verify_status = LearnwareVerifyStatus.FAIL
                pass

            with zipfile.ZipFile(learnware_processed_filename, "w") as zip_ref:
                for root, dirs, files in os.walk(extract_path):
                    for file in files:
                        if file.endswith(".pyc"):
                            continue
                        zip_ref.write(os.path.join(root, file), arcname=file)
                        pass
                    pass
                pass
            pass

        if verify_status == LearnwareVerifyStatus.SUCCESS:
            try:
                # internal service should not use proxy
                os.environ.pop("http_proxy", "")
                original_proxy = os.environ.pop("https_proxy", "")
                restful_wrapper.add_learnware_verified(learnware_id)

                # restore proxy
                os.environ["http_proxy"] = original_proxy
                os.environ["https_proxy"] = original_proxy

            except Exception as e:
                verify_status = LearnwareVerifyStatus.FAIL
                command_output += "\n\n" + str(e)
                pass
            pass

        if verify_status == LearnwareVerifyStatus.SUCCESS:
            os.remove(learnware_filename)
            os.remove(semantic_spec_filename)
            os.remove(learnware_processed_filename)
            pass

        dbops.update_learnware_verify_result(learnware_id, verify_status, command_output)

        context.logger.info(f"Finish to verify learnware: {learnware_id}")
        pass
    pass


def main(num_worker):
    context.init_database()
    context.init_logger()
    if len(context.config["verify_proxy"]) > 0:
        context.logger.info("set proxy: " + context.config["verify_proxy"])
        proxy_url = context.config["verify_proxy"]
        os.environ["http_proxy"] = proxy_url
        os.environ["https_proxy"] = proxy_url
        pass

    dbops.reset_learnware_verify_status()

    waiting_queue = queue.Queue()

    workers = []
    for i in range(num_worker):
        worker = mp.Process(target=worker_process_func, args=(waiting_queue, os.environ.copy()))
        worker.start()

        workers.append(worker)
        pass

    while True:
        learnware_ids = dbops.get_unverified_learnware()
        for learnware_id in learnware_ids:
            dbops.update_learnware_verify_status(learnware_id, LearnwareVerifyStatus.QUEUE)
            waiting_queue.put(learnware_id)
            pass

        time.sleep(1)
        pass
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-worker", type=int, default=1)

    args = parser.parse_args()
    num_worker = args.num_worker

    main(num_worker)
