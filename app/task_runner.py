from queue import Queue
from threading import Thread, Event
import json
import os
from flask import current_app

class ThreadPool:
    def __init__(self):
        env_num_threads = os.environ.get("TP_NUM_OF_THREADS")
        sys_threads = os.cpu_count() or 1 # if returns None, use at least 1 thread
        if env_num_threads is not None:
            try:
                num_threads = int(env_num_threads)
            except ValueError: # Cannot convert string to integer
                num_threads = sys_threads
        else:
            num_threads = sys_threads

        self.num_threads = min(num_threads, sys_threads) # hardware limit
        self.queue = Queue()
        self.shutdown = Event()

    def start(self):
        """ Create and run threads """
        for _ in range(self.num_threads):
            thread = TaskRunner(self.queue, self.shutdown)
            thread.start()

class TaskRunner(Thread):
    def __init__(self, queue, shutdown):
        # TODO: init necessary data structures
        Thread.__init__(self)
        self.queue: Queue = queue
        self.shutdown: Event = shutdown

    def run(self):
        while not self.shutdown.is_set():
            # TODO
            # Get pending job
            job = self.queue.get()
            job_id = job["id"]
            job_type = job["type"]
            job_question = job["question"]

            data_ingestor = current_app.data_ingestor
            
            if job_type == "states_mean":
                result = data_ingestor.states_mean(job_question)
            elif job_type == "state_mean":
                result = data_ingestor.state_mean(job_question)
            elif job_type == "best5":
                result = data_ingestor.best5(job_question)
            elif job_type == "worst5":
                result = data_ingestor.worst5(job_question)
            elif job_type == "global_mean":
                result = data_ingestor.global_mean(job_question)
            elif job_type == "diff_from_mean":
                result = data_ingestor.diff_from_mean(job_question)
            elif job_type == "state_diff_from_mean":
                result = data_ingestor.state_diff_from_mean(job_question)
            elif job_type == "mean_by_category":
                result = data_ingestor.mean_by_category(job_question)
            elif job_type == "state_mean_by_category":
                result = data_ingestor.state_mean_by_category(job_question)

            file_path = f"results/job_{job_id}.json"
            with open(file_path, 'w') as f:
                json.dump(result, f)
