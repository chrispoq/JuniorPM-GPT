from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Your JIRA config
JIRA_URL = "https://poqcommerce.atlassian.net"
API_TOKEN = "ATATT3xFfGF0mzeWNpeLkWZ1r6Z_08h6b_uY4-FJYzLwVwl475wRnDj0DqYsK3eVD32q1hoIXAZnNez7u71163cW_6tQdQmT45cMMJm2hmJu5C8S79gPy7BmxKcc0S2t0bA3osBFdWBOuwDUOao4-NdFbmHw5lmVJ3yLTh8WKNwX9sPV7CG5pOI=3AE6ABA1"
EMAIL = "chris@poqcommerce.com"

@app.route("/create-jira", methods=["POST"])
def create_jira():
    data = request.json
    payload = {
        "fields": {
            "project": {"key": data["projectKey"]},
            "summary": data["summary"],
            "description": data["description"],
            "issuetype": {"name": data["issueType"]}
        }
    }
    res = requests.post(
        f"{JIRA_URL}/rest/api/3/issue",
        json=payload,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN),
        headers={"Accept": "application/json", "Content-Type": "application/json"}
    )
    return jsonify(res.json()), res.status_code

if __name__ == "__main__":
    app.run(port=5000)
