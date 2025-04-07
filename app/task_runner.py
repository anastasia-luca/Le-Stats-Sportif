''' Thread Pool Class for creating and running threads '''
import os
import json
from queue import Queue
from threading import Thread
from app.barrier import SimpleBarrier

class ThreadPool:
    ''' Class for managing threads '''
    def __init__(self):
        ''' Initialize ThreadPool instance '''
        self.num_threads = self.get_num_threads()
        self.queue = Queue()
        self.shutdown = False
        self.barrier = SimpleBarrier(self.num_threads + 1)
        self.lst_done_jobs = []

    def start(self):
        """ Create and start threads """
        for _ in range(self.num_threads):
            thread = TaskRunner(self.queue, self.shutdown, self.barrier, self.lst_done_jobs)
            thread.start()

    def get_num_threads(self):
        ''' Return the number of threads '''
        env_num_threads = os.environ.get("TP_NUM_OF_THREADS")
        sys_threads = os.cpu_count() or 1 # if returns None, use at least 1 thread
        if env_num_threads is not None:
            try:
                num_threads = int(env_num_threads)
            except ValueError: # Cannot convert string to integer
                num_threads = sys_threads
        else:
            num_threads = sys_threads
        num_threads = min(num_threads, sys_threads) # hardware limit
        return num_threads

class TaskRunner(Thread):
    ''' Thread that process a job from queue '''
    def __init__(self, queue, shutdown, barrier, done_jobs):
        ''' Initialize necessary data structures '''
        Thread.__init__(self)
        self.queue: Queue = queue
        self.shutdown: bool = shutdown
        self.barrier: SimpleBarrier = barrier
        self.lst_done_jobs: list = done_jobs

    def run(self):
        ''' Wait until csv is processed, then process a job from queue '''
        self.barrier.wait()
        from app import webserver
        self.data_ingestor = webserver.data_ingestor

        while True:
            # Get pending job from the queue
            job = self.queue.get()
            if job is None: # Thread exits loop
                break
            job_id = job["id"]
            job_type = job["type"]
            job_question = job["data"]["question"]
            try:
                job_state = job["data"]["state"]
            except KeyError:
                pass

            # Process job based on its type
            result = None
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

            # Write the result to JSON file
            file_path = f"results/job_{job_id}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result, f)
            # Add the done job in list after writing the result in file
            self.lst_done_jobs.append(job_id)
