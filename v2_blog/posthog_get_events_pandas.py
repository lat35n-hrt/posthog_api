# v2_blog/posthog_get_events_pandas.py
from asyncio import events
import string
from dotenv import load_dotenv
import os
import requests
import pandas as pd

load_dotenv()  # loading .env file

def fetch_and_save_csv(csv_path: str):

    api_key = os.getenv("POSTHOG_PERSONAL_API_KEY")
    host = os.getenv("POSTHOG_HOST")
    project_id = os.getenv("POSTHOG_PROJECT_ID")
    api_events_url = f"{host}/api/projects/{project_id}/events"
    filter_event = os.getenv("POSTHOG_FILTER_EVENT")

    if not all([api_key, project_id, host]):
        raise ValueError("Required .env info (API KEY, Project ID or host) are missing")

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    params = {
        "limit": 500  # latest 500 events
    }

    response = requests.get(api_events_url, headers=headers, params=params)
    events = response.json().get("results", [])

    # print("Fetched event names:", [e.get("event") for e in events])

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
    df['current_url'] = df['properties'].apply(
    lambda x: x.get('$current_url', 'N/A') if isinstance(x, dict) else 'N/A')
    # df['title'] = df['properties'].apply(
    # lambda x: x.get('$title', 'N/A') if isinstance(x, dict) else 'N/A')
    df['referrer'] = df['properties'].apply(
    lambda x: x.get('$referrer', 'N/A') if isinstance(x, dict) else 'N/A')

    # --- aggregation ---
    df_temp = df.copy()
    df_temp['timestamp'] = pd.to_datetime(
        df_temp['timestamp'],
        utc=True,           # +00:00 UTC
        errors="coerce"     # NaT if invalid parsing
    )

    stats = {
        "unique_users": df_temp['distinct_id'].nunique(),
        "total_pageviews": len(df_temp),
        "period_start": df_temp['timestamp'].min().strftime("%Y-%m-%d %H:%M"),
        "period_end": df_temp['timestamp'].max().strftime("%Y-%m-%d %H:%M"),
        "top_pages": df_temp['current_url'].value_counts().head(10)
    }

    print("=== Event Statistics ===")
    print(f"Unique Users: {stats['unique_users']}")
    print(f"Total Pageviews: {stats['total_pageviews']}")
    print(f"Period: {stats['period_start']} to {stats['period_end']}")
    print("Top 10 Pages:")
    print(stats['top_pages'])


    # --- Rename columns for better readability ---
    df.rename(columns={"timestamp": "Timestamp"}, inplace=True)
    df.rename(columns={"distinct_id": "User ID"}, inplace=True)
    df.rename(columns={"event": "Event"}, inplace=True)
    df.rename(columns={"current_url": "URL"}, inplace=True)
    df.rename(columns={"referrer": "Referrer"}, inplace=True)
    df.rename(columns={"timestamp": "Timestamp"}, inplace=True)

    # Save enhanced CSV
    df[["Timestamp", "User ID", "Event", "URL", "Referrer"]].to_csv(csv_path, index=False)

    print(f"✅ Events saved to CSV: {csv_path}")


    #df and stats return to generate additional report
    return df, stats


if __name__ == "__main__":
    fetch_and_save_csv("debug_events.csv")