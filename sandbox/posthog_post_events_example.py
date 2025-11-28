from dotenv import load_dotenv
import os
import requests

# Loading .env file
load_dotenv()

# Required env variables
api_key = os.getenv("POSTHOG_API_KEY")
host = os.getenv("POSTHOG_HOST")
# project_id = os.getenv("POSTHOG_PROJECT_ID")
filter_event = os.getenv("POSTHOG_FILTER_EVENT")
distinct_id = os.getenv("POSTHOG_DISTINCT_ID")
action = os.getenv("POSTHOG_ACTION")
page = os.getenv("POSTHOG_PAGE")

# Validation for env variables
if not all([api_key, host, filter_event, distinct_id, action, page]):
    raise ValueError("Required .env values are missing")

# API Endpoint
url = f"{host}/capture"

# POST Requests
res = requests.post(url, json={
    "api_key": api_key,
    "event": filter_event,
    "distinct_id": distinct_id,
    "properties": {
        "action": action,
        "page": page
    }
})

# Response confirmation - expected: 200, {"status":"Ok"}
print(res.status_code)
print(res.text)