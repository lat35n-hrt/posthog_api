from dotenv import load_dotenv
import os
import requests
import pandas as pd

load_dotenv()  # loading .env file

api_key = os.getenv("POSTHOG_PERSONAL_API_KEY")
host = os.getenv("POSTHOG_HOST")
project_id = os.getenv("POSTHOG_PROJECT_ID")
url = f"{host}/api/projects/{project_id}/events"
filter_event = os.getenv("POSTHOG_FILTER_EVENT")
csv_path =  os.getenv("CSV_PATH")

if not all([api_key, project_id, host]):
    raise ValueError("Required .env info (API KEY, Project ID or host) are missing")

headers = {
    "Authorization": f"Bearer {api_key}"
}

params = {
    "limit": 10  # latest 10 events
}

response = requests.get(url, headers=headers, params=params)
events = response.json().get("results", [])

filtered = [e for e in events if e["event"] == filter_event]

df = pd.DataFrame(filtered)
if not df.empty:
    print(df[["timestamp", "distinct_id", "event"]])
else:
    print("DataFrame is empty.: {filter_event}")

 # Save CSV
df[["timestamp", "distinct_id", "event"]].to_csv(csv_path, index=False)
print(f"✅ Events saved to CSV: {csv_path}")