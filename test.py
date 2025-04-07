import requests, time

for i in range(100):
    res = requests.post(f"http://127.0.0.1:5000/api/mean_by_category", json={"question": "Percent of adults who report consuming fruit less than one time daily"})
    # res = requests.get(f"http://127.0.0.1:5000/api/get_results/{res.json()['job_id']}")
# print(res.json())

shut = requests.get(f"http://127.0.0.1:5000/api/jobs")
print(shut.json())
shut = requests.get(f"http://127.0.0.1:5000/api/num_jobs")
print(shut.json())
