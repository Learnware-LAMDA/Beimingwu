import time
import context
import lib.database_operations as dbops
import queue
import multiprocessing.dummy as mp
import argparse
import os
import lib.command_executor as command_executor
from database.base import LearnwareVerifyStatus
import json
import lib.restful_wrapper as restful_wrapper


def worker_process_func(q: queue.Queue):

    while True:
        learnware_id = q.get()
        context.logger.info(f"Start to verify learnware: {learnware_id}")
        
        dbops.update_learnware_verify_status(learnware_id, LearnwareVerifyStatus.PROCESSING)
        learnware_filename = context.get_learnware_verify_file_path(learnware_id)
        semantic_spec_filename = learnware_filename[:-4] + ".json"

        process_result_filename = learnware_filename + ".result"
        
        verify_script = os.path.join('scripts', 'verify_learnware.py')
        verify_command = (
            f"python3 {verify_script} --learnware-path {learnware_filename}"
            f" --semantic-path {semantic_spec_filename}"
            f" --result-file-path {process_result_filename} --create-env")
        
        try:
            command_output = command_executor.execute_shell(verify_command, timeout=context.config.verify_timeout)
        except Exception as e:
            context.logger.exception(e)
            command_output = str(e)
            pass

        # the learnware my be deleted
        if not dbops.check_learnware_exist(learnware_id=learnware_id):
            context.logger.info(f'learnware is deleted, no need to process: {learnware_id}')
            continue
        
        verify_sucess = True

        if not os.path.exists(process_result_filename):
            verify_sucess = False
            pass
        else:
            try:
                with open(process_result_filename, 'r') as f:
                    verify_result = json.load(f)
                    pass

                if verify_result['result_code'] != 'SUCCESS':
                    verify_sucess = False
                    pass
            except Exception:
                verify_sucess = False
                pass

            os.remove(process_result_filename)
            pass

        if verify_sucess:
            verify_status = LearnwareVerifyStatus.SUCCESS
        else:
            verify_status = LearnwareVerifyStatus.FAIL
            pass
        
        if verify_status == LearnwareVerifyStatus.SUCCESS:
            try:
                restful_wrapper.add_learnware_verified(learnware_id)
            except Exception as e:
                verify_status = LearnwareVerifyStatus.FAIL
                command_output += "\n\n" + str(e)
                pass
            pass

        if verify_status == LearnwareVerifyStatus.FAIL:
            dbops.update_learnware_verify_result(learnware_id, verify_status, command_output)
        else:
            dbops.update_learnware_verify_result(learnware_id, verify_status, command_output)
            pass

        context.logger.info(f"Finish to verify learnware: {learnware_id}")
        pass
    pass


def main(num_worker):
    context.init_database()
    context.init_logger()

    dbops.reset_learnware_verify_status()

    waiting_queue = queue.Queue()

    workers = []
    for i in range(num_worker):
        worker = mp.Process(target=worker_process_func, args=(waiting_queue,))
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-worker', type=int, default=2)
    
    args = parser.parse_args()
    num_worker = args.num_worker

    main(num_worker)

