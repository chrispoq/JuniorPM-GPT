import os
from flask import Flask, request, jsonify, abort
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Load secrets from environment
JIRA_URL = os.getenv("JIRA_URL")
API_TOKEN = os.getenv("API_TOKEN")
EMAIL = os.getenv("EMAIL")
GPT_SECRET = os.getenv("GPT_SECRET")

@app.route("/create-jira", methods=["POST"])
def create_jira():
    auth_header = request.headers.get("X-GPT-SECRET")
    if auth_header != GPT_SECRET:
        abort(403, description="Forbidden: Invalid GPT secret")

    data = request.json or {}

    # Validate required fields
    required_fields = ["summary", "description", "projectKey", "issueType"]
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

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
    
    print("[JIRA PAYLOAD]", json.dumps(payload, indent=2), flush=True)
    print("[JIRA RESPONSE]", res.status_code, res.text, flush=True)


    return jsonify(res.json()), res.status_code

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

