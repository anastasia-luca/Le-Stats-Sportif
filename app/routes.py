from app import webserver
from flask import request, jsonify

import os
import json

def register_job(request_type):
    # Get request data
    data = request.json
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
    # Return associated job_id
    return jsonify({"job_id": job_id})

def res_for(file_path):
    file = open(file_path, "r")
    data = file.read()
    file.close()
    return data

def get_job_status(job_id):
    file_path = f"results/{job_id}.json"
    if not os.path.exists(file_path):
        # The result is not done yet
        return "running"
    else:
        return "done"

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405
    
@webserver.route('/api/jobs', methods=['GET'])
def all_jobs():
    jobs = [{f"job_id_{i}": get_job_status(i)} for i in range(webserver.job_counter)]
    # Returns a json that contains a list of all job_ids and its status
    return jsonify({
        "status": "done",
        "data": jobs
    })


@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    files = os.listdir("results")
    # difference of all jobs and done jobs = running jobs
    return webserver.job_counter - len(files)

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")
    # Check if job_id is valid
    if job_id >= webserver.job_counter:
        return jsonify({
            "status": "error",
            "reason": "Invalid job_id"
        })
    
    file_path = f"results/{job_id}.json"
    if not os.path.exists(file_path):
        # The result is not done yet
        return jsonify({"status": "running"})
    
    # Get the result from file
    res = res_for(file_path)

    return jsonify({
        "status": "done",
        "data": res
    })

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    return register_job("states_mean")

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    return register_job("state_mean")

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    return register_job("best5")

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    return register_job("worst5")

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    return register_job("global_mean")

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    return register_job("diff_from_mean")

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    return register_job("state_diff_from_mean")

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    return register_job("mean_by_category")

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    return register_job("state_mean_by_category")

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
