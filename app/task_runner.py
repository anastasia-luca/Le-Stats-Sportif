from queue import Queue
from threading import Thread, Event
import time
import os

class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        # Note: the TP_NUM_OF_THREADS env var will be defined by the checker
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
        self.queue = Queue() # queue for jobs
        self.shutdown = Event()

    def start(self):
        """ Create and run threads """
        for _ in range(self.num_threads):
            thread = TaskRunner(self.queue, self.shutdown)
            thread.start()



class TaskRunner(Thread):
    def __init__(self, queue, shutdown):
        # TODO: init necessary data structures
        super().__init__()
        self.queue = queue
        self.shutdown = shutdown

    def run(self):
        while not self.shutdown.is_set():
            # TODO
            # Get pending job
            job = self.queue.get()
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            pass
