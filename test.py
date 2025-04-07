import requests, time

res = requests.post(f"http://127.0.0.1:5000/api/state_mean_by_category", json={"question": "Percent of adults who engage in no leisure-time physical activity", "state": "Maryland"})
time.sleep(0.2)
res = requests.get(f"http://127.0.0.1:5000/api/get_results/{res.json()['job_id']}")