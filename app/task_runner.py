from queue import Queue
from threading import Thread, Event
import json
import os
from app.barrier import SimpleBarrier
from app.data_ingestor import DataIngestor

class ThreadPool:
    def __init__(self, data_ingestor: DataIngestor):
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
        self.barrier = SimpleBarrier(self.num_threads + 1)
        self.data_ingestor = None

    def set_data_ingestor(self, data_ingestor):
        self.data_ingestor: DataIngestor = data_ingestor

    def start(self):
        """ Create and run threads """
        for _ in range(self.num_threads):
            thread = TaskRunner(self.queue, self.shutdown, self.barrier, self.data_ingestor)
            thread.start()

class TaskRunner(Thread):
    def __init__(self, queue, shutdown, barrier, data_ingestor):
        # TODO: init necessary data structures
        Thread.__init__(self)
        self.queue: Queue = queue
        self.shutdown: Event = shutdown
        self.barrier: SimpleBarrier = barrier
        self.data_ingestor: DataIngestor = data_ingestor

    def run(self):
        # Wait until csv is processed
        self.barrier.wait()

        while True:
            # Get pending job
            job = self.queue.get()
            job_id = job["id"]
            job_type = job["type"]
            job_question = job["data"]["question"]
            job_state = job["data"]["state"]
            
            if job_type == "states_mean":
                result = self.data_ingestor.states_mean(job_question)
            elif job_type == "state_mean":
                result = self.data_ingestor.state_mean(job_question, job_state)
            elif job_type == "best5":
                result = self.data_ingestor.best5(job_question)
            elif job_type == "worst5":
                result = self.data_ingestor.worst5(job_question)
            elif job_type == "global_mean":
                result = self.data_ingestor.global_mean(job_question)
            elif job_type == "diff_from_mean":
                result = self.data_ingestor.diff_from_mean(job_question)
            elif job_type == "state_diff_from_mean":
                result = self.data_ingestor.state_diff_from_mean(job_question, job_state)
            elif job_type == "mean_by_category":
                result = self.data_ingestor.mean_by_category(job_question)
            elif job_type == "state_mean_by_category":
                result = self.data_ingestor.state_mean_by_category(job_question, job_state)

            file_path = f"results/job_{job_id}.json"
            with open(file_path, 'w') as f:
                json.dump(result, f)
