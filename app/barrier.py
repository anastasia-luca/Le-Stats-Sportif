""" Implementation of a barrier """
from threading import Event, Lock

class SimpleBarrier():
    ''' Synchronized barrier '''
    def __init__(self, num_threads):
        ''' Initialize barrier instance '''
        self.num_threads = num_threads
        self.count_threads = self.num_threads
        self.count_lock = Lock()
        self.threads_event = Event()

    def wait(self):
        ''' Wait until all threads have reached the barrier '''
        with self.count_lock:
            self.count_threads -= 1
            if self.count_threads == 0:
                self.threads_event.set()
        self.threads_event.wait()

    def __len__(self):
        ''' Returns the number of threads'''
        return self.num_threads
