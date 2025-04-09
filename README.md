# Homework 1 - Le Stats Sportif
__Luca Anastasia, 332CC__

The purpose of this project is to implement a _Flask-based server_ for processing health and nutrition statistics from a dataset using a thread pool, graceful shutdown, and log activity via RotatingFileHandler.

## === Implementation ===
1. `__init__.py` – __App Initialization & Logging__
   - Creates Flask app (`webserver`)
   - Initializes `ThreadPool` and starts the threads
   - Parses the CSV file via `DataIngestor`
   - Setting up the __logging__:
     - Stored logs in `logs/webserver.log`
     - Used `RotatingFileHandler` (5 backups, 1MB max)
     - Prints all routes entries/exists with INFO level
     - Used UTC\GMT timestamps.

2. `task_runner.py` - __ThreadPool & Job Execution__
   - `ThreadPool` manages a queue and multiple `TaskRunner` threads
   - Threads wait on a custom barrier (`SimpleBarrier` imported from lab 3) to ensure all threads start only after the CSV is loaded
   - After barrier, each thread enters a continuous loop where gets a job from queue and execute the request according to iyts type. If a thread dequeues a `None`,  it interprets it as a shutdown signal and gracefully exits the processing loop.
   - Then, each thread writes the result to `results/job_<id>.json`
   - Used a `lst_done_jobs` list to store the job_ids that are already done to avoid concurrency and eronated results.

3. `data_ingestor.py` - __Data Parsing and Analysis__
- Loads the CSV file using `pandas`
- Implemented functions for API requests like:
  - `states_mean()`, `state_mean()`
  - `best5()`, `worst5()`, etc
  - I used `pandas` to filter the `DataFrame` based on request conditions, and applied `groupby` to aggregate data per category. Each function returns a dictionary, either through to_dict() or dictionary comprehension.

4. `routes.py` - __HTTP Routes & API__
   - Defines Flask endpoints like: `/api/states_mean` ... `/api/state_mean_by_category`, `/api/get_results/<job_id>`
   - In addition implemented:
     - `/api/job` - lists all jobs and their status in JSON format
     - `/api/num_jobs` - number of running jobs
     - `/api/graceful_shutdown` - stops the server from accepting new processing requests. Upon receiving a shutdown request, a shutdown flag is set, and a number of sentinel values (None), equal to the number of threads, are inserted into the queue. These act as termination signals: when a thread dequeues a None, it exits its processing loop, ensuring all active jobs are completed while no new ones are accepted.

5. `barrier.py` - __Thread Synchronization__
   - Implements a barrier using `Event` and `Lock`
   - Structure from lab3 (https://ocw.cs.pub.ro/courses/asc/laboratoare/03)

## === Unittesting ===

To validate the implementation of the data processing functions, I used Python's `unittest` framework. The test data comes from a smaller CSV file that I created myself. Each test checks a specific function of the DataIngestor class, comparing the actual output to what I calculated.
