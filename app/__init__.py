import os
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

if not os.path.exists('results'):
    os.mkdir('results')

webserver = Flask(__name__)
webserver.task_runner = ThreadPool()

webserver.task_runner.start()

data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv", webserver.task_runner.barrier)
webserver.task_runner.set_data_ingestor(data_ingestor)

webserver.job_counter = 1

from app import routes
