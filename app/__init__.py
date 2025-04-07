''' Initialize the Flask application '''
import os
import time
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

if not os.path.exists('results'):
    os.mkdir('results')

if not os.path.exists('logs'):
    os.mkdir('logs')

# ===== Logging setup =====
# Create a logger
logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)

# Setup rotating file handler
handler = RotatingFileHandler('logs/webserver.log', maxBytes=1024*1024, backupCount=5)

# Create the formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
formatter.converter = time.gmtime  # Use UTC for timestamps
# Assign formatter to handler
handler.setFormatter(formatter)

# Assign handler to logger
logger.addHandler(handler)

# ===== Flask app setup =====
webserver = Flask(__name__)

webserver.logger = logger

webserver.task_runner = ThreadPool()

webserver.task_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv",
                                       webserver.task_runner.barrier)

webserver.job_counter = 1

logger.info("The app has started!")

from app import routes
