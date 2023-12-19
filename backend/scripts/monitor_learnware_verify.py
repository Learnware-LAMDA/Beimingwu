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
import tempfile
import lib.engine as engine_utils
from typing import Tuple
import learnware.utils
from learnware.market import CondaChecker, EasyStatChecker, EasySemanticChecker
from learnware.learnware import get_learnware_from_dirpath
import traceback
from lib import redis_utils
from lib import sensitive_words_utils


def verify_learnware_with_conda_checker(
    learnware_id: str, learnware_path: str, semantic_specification: dict
) -> Tuple[bool, str]:
    verify_sucess = True
    command_output = "Success"

    # verify initiate
    try:
        learnware = get_learnware_from_dirpath(
            id=learnware_id, semantic_spec=semantic_specification, learnware_dirpath=learnware_path, ignore_error=False
        )
    except Exception as e:
        verify_sucess = False
        command_output = f"initiate learnware failed."
        command_output += "\r\n" + traceback.format_exc()
        return verify_sucess, command_output

    # verify easy checker
    try:
        semantic_checker = EasySemanticChecker()
        check_result, check_message = semantic_checker(learnware=learnware)
        if check_result == EasySemanticChecker.INVALID_LEARNWARE:
            verify_sucess = False
            command_output = "semantic checker does not pass"
            command_output += "\n" + check_message
            pass

        stat_checker = CondaChecker(inner_checker=EasyStatChecker())
        check_result, check_message = stat_checker(learnware=learnware)
        if verify_sucess and check_result == EasyStatChecker.INVALID_LEARNWARE:
            verify_sucess = False
            command_output = "conda checker does not pass"
            command_output += "\n" + check_message

    except Exception as e:
        verify_sucess = False
        command_output = f"Statistical checker runtime error"
        command_output += "\r\n" + traceback.format_exc()

    if not verify_sucess:
        return verify_sucess, command_output

    # verify sensitive words
    if context.sensitive_pattern is not None:
        for filname in os.listdir(learnware_path):
            if any([filname.endswith(suffix) for suffix in (".txt", ".yaml", ".yml", ".json", ".py")]):
                with open(os.path.join(learnware_path, filname), "rb") as fin:
                    try:
                        file_content = fin.read().decode("utf-8")
                    except Exception as e:
                        continue

                    matches = sensitive_words_utils.search_sensitive_words(file_content, context.sensitive_pattern)
                    if len(matches) > 0:
                        return False, f"Sensitive words {','.join(matches)} in {filname}"
                    pass
                pass
            pass

        semantic_str = json.dumps(semantic_specification, ensure_ascii=False)
        matches = sensitive_words_utils.search_sensitive_words(semantic_str, context.sensitive_pattern)
        if len(matches) > 0:
            return False, f"Sensitive words {','.join(matches)} in semantic specification"
        pass

    return verify_sucess, command_output


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
        learnware_info = context.engine.learnware_organizer.get_learnware_info_from_storage(learnware_id)

        try:
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
                    # the learnware my be deleted
                    if not dbops.check_learnware_exist(learnware_id=learnware_id):
                        context.logger.info(f"learnware is deleted, no need to process: {learnware_id}")
                        continue

                    learnware.utils.zip_learnware_folder(extract_path, learnware_processed_filename)
                    pass
                final_id, final_status = context.engine.add_learnware(
                    learnware_processed_filename, semantic_specification, [], learnware_id=learnware_id
                )
                learnware_zippath = learnware_processed_filename

            else:
                # it is in the learnware engine

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

                verify_success, command_output = verify_learnware_with_conda_checker(
                    learnware_id, learnware_dirpath, semantic_specification
                )
                pass

        except Exception as e:
            context.logger.exception(e)
            verify_status = LearnwareVerifyStatus.WAITING
            command_output = "\n\n" + str(e)
            pass

        # the learnware my be deleted
        if not dbops.check_learnware_exist(learnware_id=learnware_id):
            context.logger.info(f"learnware is deleted, no need to process: {learnware_id}")
            continue

        if verify_success:
            verify_status = LearnwareVerifyStatus.SUCCESS
            learnware_check_status = BaseChecker.USABLE_LEARWARE
        else:
            verify_status = LearnwareVerifyStatus.FAIL
            pass

        context.engine.update_learnware(
            learnware_id, learnware_zippath, semantic_specification, [], learnware_check_status
        )

        if verify_status == LearnwareVerifyStatus.SUCCESS:
            if learnware_filename is not None:
                os.remove(learnware_filename)
                os.remove(semantic_spec_filename)
                os.remove(learnware_processed_filename)
                pass
            pass

        dbops.update_learnware_verify_result(learnware_id, verify_status, command_output)
        redis_utils.publish_reload_learnware(learnware_id)
        context.logger.info(f"Finish to verify learnware: {learnware_id}")


def main(num_worker):
    context.init_database()
    context.init_logger(target="file")
    context.init_engine()
    context.init_redis()
    context.init_sensitive_words()

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
