import time
import context
import lib.database_operations as dbops
import lib.common_utils as common_utils
import queue
import multiprocessing.dummy as mp
import argparse
import os
import functools
import lib.command_executor as command_executor
from database.base import LearnwareVerifyStatus
from learnware.market import BaseChecker
import json
import lib.restful_wrapper as restful_wrapper
import tempfile
import zipfile
import lib.engine as engine_utils
import yaml
import shutil
from typing import Tuple
import learnware.utils
from learnware.market import CondaChecker, EasyStatChecker, EasySemanticChecker
from learnware.learnware import get_learnware_from_dirpath


def verify_learnware_with_conda_checker(
    learnware_id: str, learnware_path: str, semantic_specification: dict
) -> Tuple[bool, str]:
    verify_sucess = True
    command_output = ""
    try:
        learnware = get_learnware_from_dirpath(
            id=learnware_id, semantic_spec=semantic_specification, learnware_dirpath=learnware_path, ignore_error=False
        )
    except Exception as e:
        verify_sucess = False
        command_output = f"initiate learnware failed due to {str(e)}"
        return verify_sucess, command_output

    try:
        semantic_checker = EasySemanticChecker()
        if semantic_checker(learnware=learnware) == EasySemanticChecker.INVALID_LEARNWARE:
            verify_sucess = False
            command_output = "semantic checker does not pass"

        stat_checker = CondaChecker(inner_checker=EasyStatChecker())
        if verify_sucess and stat_checker(learnware=learnware) == EasyStatChecker.INVALID_LEARNWARE:
            verify_sucess = False
            command_output = "conda checker does not pass"

    except Exception as e:
        verify_sucess = False
        command_output = f"Statistical checker runtime error due to {str(e)}"

    return verify_sucess, command_output


def call_internal_service(func):
    os.environ.pop("http_proxy", "")
    original_proxy = os.environ.pop("https_proxy", "")

    try:
        return func()
    finally:
        # restore proxy
        os.environ["http_proxy"] = original_proxy
        os.environ["https_proxy"] = original_proxy
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

        try:
            learnware_info = context.engine.learnware_organizer.get_learnware_info_from_storage(learnware_id)
            learnware_check_status = BaseChecker.NONUSABLE_LEARNWARE

            if learnware_info is None:
                # it is in the upload folder, not learnware engine
                learnware_filename = context.get_learnware_verify_file_path(learnware_id)
                semantic_spec_filename = learnware_filename[:-4] + ".json"
                process_result_filename = learnware_filename + ".result"
                learnware_processed_filename = learnware_filename[:-4] + "_processed.zip"

                with open(semantic_spec_filename, "r") as fin:
                    semantic_specification = json.load(fin)

                with tempfile.TemporaryDirectory(dir=context.config["temp_path"]) as tmpdir:
                    extract_path = tmpdir
                    engine_utils.repack_learnware_folder(
                        learnware_filename, extract_path, learnware_id, semantic_specification
                    )

                    verify_success, command_output = verify_learnware_with_conda_checker(
                        learnware_id, extract_path, semantic_specification
                    )
                    learnware.utils.zip_learnware_folder(extract_path, learnware_processed_filename)
            else:
                learnware_filename = None
                semantic_spec_filename = None
                learnware_processed_filename = None
                # we need repack the zip folder because the learnware may be updated

                learnware_dirpath = learnware_info["folder_path"]
                learnware_zippath = learnware_info["zip_path"]
                semantic_specification = learnware_info["semantic_spec"]

                common_utils.delete_folder_content(learnware_dirpath)
                engine_utils.repack_learnware_folder(
                    learnware_zippath, learnware_dirpath, learnware_id, semantic_specification
                )
                os.remove(learnware_zippath)
                learnware.utils.zip_learnware_folder(learnware_dirpath, learnware_zippath)

                # it is in the learnware engine
                verify_success, command_output = verify_learnware_with_conda_checker(
                    learnware_id, learnware_dirpath, semantic_specification
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

        except Exception as e:
            context.logger.exception(e)
            verify_status = LearnwareVerifyStatus.WAITING
            command_output = "\n\n" + str(e)
            pass

        try:
            call_internal_service(
                functools.partial(restful_wrapper.add_learnware_verified, learnware_id, learnware_check_status)
            )
        except Exception as e:
            # Add engine database failed, need to retry
            context.logger.exception(e)
            verify_status = LearnwareVerifyStatus.WAITING
            command_output += "\n\n" + str(e)
            pass

        if verify_status == LearnwareVerifyStatus.SUCCESS:
            if learnware_filename is not None:
                os.remove(learnware_filename)
                os.remove(semantic_spec_filename)
                os.remove(learnware_processed_filename)
                pass
            pass

        dbops.update_learnware_verify_result(learnware_id, verify_status, command_output)
        context.logger.info(f"Finish to verify learnware: {learnware_id}")


def main(num_worker):
    context.init_database()
    context.init_logger()
    context.init_engine()

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
