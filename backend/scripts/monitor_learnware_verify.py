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
from learnware.market import BaseChecker
import json
import lib.restful_wrapper as restful_wrapper
import tempfile
import zipfile
import lib.engine as engine_ops
import yaml
import shutil
from typing import Tuple
import learnware.utils
from learnware.market import CondaChecker, EasyStatChecker
from learnware.learnware import get_learnware_from_dirpath


def verify_learnware_with_conda_checker(
    learnware_id: str, learnware_path: str, semantic_spec_filename: str
) -> Tuple[bool, str]:
    verify_sucess = True
    command_output = ""
    try:
        with open(semantic_spec_filename, "r") as fin:
            semantic_specification = json.load(fin)
        learnware = get_learnware_from_dirpath(
            id=learnware_id, semantic_spec=semantic_specification, learnware_dirpath=learnware_path, ignore_error=False
        )
    except Exception as e:
        verify_sucess = False
        command_output = f"initiate learnware failed due to {str(e)}"
        return verify_sucess, command_output

    try:
        stat_checker = CondaChecker(inner_checker=EasyStatChecker())
        if stat_checker(learnware=learnware) == EasyStatChecker.INVALID_LEARNWARE:
            verify_sucess = False
            command_output = "Statistical checker does not pass"
    except Exception as e:
        verify_sucess = False
        command_output = f"Statistical checker runtime error due to {str(e)}"

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

        dbops.update_learnware_verify_status(learnware_id, LearnwareVerifyStatus.PROCESSING)
        learnware_filename = context.get_learnware_verify_file_path(learnware_id)
        semantic_spec_filename = learnware_filename[:-4] + ".json"
        process_result_filename = learnware_filename + ".result"
        learnware_processed_filename = learnware_filename[:-4] + "_processed.zip"
        learnware_check_status = BaseChecker.NONUSABLE_LEARNWARE

        with tempfile.TemporaryDirectory(dir=context.config["temp_path"]) as tmpdir:
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

            verify_success, command_output = verify_learnware_with_conda_checker(
                learnware_id, extract_path, semantic_spec_filename
            )

            # the learnware my be deleted
            if not dbops.check_learnware_exist(learnware_id=learnware_id):
                context.logger.info(f"learnware is deleted, no need to process: {learnware_id}")
                continue

            if verify_success:
                verify_status = LearnwareVerifyStatus.SUCCESS
                learnware_check_status = BaseChecker.USABLE_LEARWARE
            else:
                verify_status = LearnwareVerifyStatus.FAIL

            learnware.utils.zip_learnware_folder(extract_path, learnware_processed_filename)

        try:
            # internal service should not use proxy
            os.environ.pop("http_proxy", "")
            original_proxy = os.environ.pop("https_proxy", "")
            restful_wrapper.add_learnware_verified(learnware_id, learnware_check_status)

            # restore proxy
            os.environ["http_proxy"] = original_proxy
            os.environ["https_proxy"] = original_proxy

        except Exception as e:
            verify_status = LearnwareVerifyStatus.FAIL
            command_output += "\n\n" + str(e)

        if verify_status == LearnwareVerifyStatus.SUCCESS:
            os.remove(learnware_filename)
            os.remove(semantic_spec_filename)
            os.remove(learnware_processed_filename)

        dbops.update_learnware_verify_result(learnware_id, verify_status, command_output)
        context.logger.info(f"Finish to verify learnware: {learnware_id}")


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
