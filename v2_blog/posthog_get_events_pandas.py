from asyncio import events
from dotenv import load_dotenv
import os
import requests
import pandas as pd

load_dotenv()  # loading .env file

def fetch_and_save_csv(csv_path: str):

    api_key = os.getenv("POSTHOG_PERSONAL_API_KEY")
    host = os.getenv("POSTHOG_HOST")
    project_id = os.getenv("POSTHOG_PROJECT_ID")
    url = f"{host}/api/projects/{project_id}/events"
    filter_event = os.getenv("POSTHOG_FILTER_EVENT")

    if not all([api_key, project_id, host]):
        raise ValueError("Required .env info (API KEY, Project ID or host) are missing")

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    params = {
        "limit": 500  # latest 500 events
    }

    response = requests.get(url, headers=headers, params=params)
    events = response.json().get("results", [])

    print("Fetched event names:", [e.get("event") for e in events])

    filtered = [e for e in events if e["event"] == filter_event]

    df = pd.DataFrame(filtered)
    if not df.empty:
        print(df[["timestamp", "distinct_id", "event"]])
    else:
        print("DataFrame is empty.: {filter_event}")

    # Save CSV
    # Original:
    # df[["timestamp", "distinct_id", "event"]].to_csv(csv_path, index=False)

    # v2_blog enhancement: add more columns
    df['url'] = df['properties'].apply(
    lambda x: x.get('$current_url', 'N/A') if isinstance(x, dict) else 'N/A')
    # df['title'] = df['properties'].apply(
    # lambda x: x.get('$title', 'N/A') if isinstance(x, dict) else 'N/A')
    df['referrer'] = df['properties'].apply(
    lambda x: x.get('$referrer', 'N/A') if isinstance(x, dict) else 'N/A')

    # v2_blog enhancement: add more columns
    df[["timestamp", "distinct_id", "event", "url", "referrer"]].to_csv(csv_path, index=False)

    print(f"✅ Events saved to CSV: {csv_path}")


if __name__ == "__main__":
    fetch_and_save_csv("debug_events.csv")