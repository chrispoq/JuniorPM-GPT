import os
from flask import Flask, request, jsonify, abort
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Load secrets from environment
JIRA_URL = os.getenv("JIRA_URL")
API_TOKEN = os.getenv("API_TOKEN")
EMAIL = os.getenv("EMAIL")
GPT_SECRET = os.getenv("GPT_SECRET")  # Add this

@app.route("/create-jira", methods=["POST"])
def create_jira():
    auth_header = request.headers.get("X-GPT-SECRET")
    if auth_header != GPT_SECRET:
        abort(403, description="Forbidden: Invalid GPT secret")

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
