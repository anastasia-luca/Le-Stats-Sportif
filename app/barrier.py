from threading import Event, Lock

class SimpleBarrier():
    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.count_threads = self.num_threads
        self.count_lock = Lock()
        self.threads_event = Event()
 
    def wait(self):
        with self.count_lock:
            self.count_threads -= 1
            if self.count_threads == 0:
                self.threads_event.set()
        self.threads_event.wait()