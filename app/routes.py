''' Webserver routes '''
import json
from flask import request, jsonify
from app import webserver

def register_job(data, request_type):
    ''' Register a new job and add it to the queue '''
    webserver.logger.info("Entered /api/%s", request_type)
    if webserver.task_runner.shutdown is True:
        return jsonify({
            "status": "error",
            "reason": "shutting down"
        })
    # Associate a job_id for request
    job_id = webserver.job_counter
    # Increment job_id counter for the next request
    webserver.job_counter += 1
    # create dictionary for every
    job = {
        "id": job_id,
        "type": request_type,
        "data": data
    }
    # Put the job in queue
    webserver.task_runner.queue.put(job)
    webserver.logger.info("Exiting with job_id_%d from /api/%s", job_id, request_type)
    # Return associated job_id
    return jsonify({"job_id": job_id})

def res_for(file_path):
    ''' Returns the result from JSON file '''
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_job_status(job_id):
    ''' Return job status '''
    if job_id in webserver.task_runner.lst_done_jobs:
        return "done"
    return "running"

@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    ''' Echo received JSON data '''
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    # Method Not Allowed
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def shutdown():
    ''' Signal shutdown '''
    if webserver.task_runner.shutdown is False:
        for _ in range(webserver.task_runner.num_threads):
            webserver.task_runner.queue.put(None)

    webserver.task_runner.shutdown = True

    if webserver.task_runner.queue.qsize() > 0:
        return jsonify({"status": "running"})
    return jsonify({"status": "done"})

@webserver.route('/api/jobs', methods=['GET'])
def all_jobs():
    ''' Return a JSON containing all job IDs with their status '''
    jobs = [{f"job_id_{i}": get_job_status(i)} for i in range(1, webserver.job_counter)]
    # Returns a json that contains a list of all job_ids and its status
    return jsonify({
        "status": "done",
        "data": jobs
    })


@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    ''' Return number of running jobs '''
    # difference of all jobs and done jobs = running jobs
    return jsonify({
        "status": "done",
        "data": {"running jobs" :
                webserver.job_counter - len(webserver.task_runner.lst_done_jobs) - 1}
    })

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    ''' Return job status or result if is done '''
    job_id = int(job_id)
    # Check if job_id is valid
    if job_id >= webserver.job_counter:
        return jsonify({
            "status": "error",
            "reason": "Invalid job_id"
        })

    if job_id not in webserver.task_runner.lst_done_jobs:
        # The result is not done yet
        return jsonify({"status": "running"})
    # Get the result from file
    file_path = f"results/job_{job_id}.json"
    res = res_for(file_path)
    return jsonify({
        "status": "done",
        "data": res
    })

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    ''' Register states_mean job '''
    return register_job(request.json, "states_mean")

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    ''' Register state_mean job '''
    return register_job(request.json, "state_mean")

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    ''' Register best5 job '''
    return register_job(request.json, "best5")

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    ''' Register worst5 job '''
    return register_job(request.json, "worst5")

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    ''' Register global_mean job '''
    return register_job(request.json, "global_mean")

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    ''' Register diff_from_mean job '''
    return register_job(request.json, "diff_from_mean")

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    ''' Register state_diff_from_mean job '''
    return register_job(request.json, "state_diff_from_mean")

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    ''' Register mean_by_category job '''
    return register_job(request.json, "mean_by_category")

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    ''' Register state_mean_by_category job '''
    return register_job(request.json, "state_mean_by_category")

@webserver.route('/')
@webserver.route('/index')
def index():
    ''' Show available route '''
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    paragraphs = "".join(f"<p>{route}</p>" for route in routes)

    msg += paragraphs
    return msg

def get_defined_routes():
    ''' Return list of defined endpoints '''
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
