

## PostHog API Integration (Event Sender & Getter)



## Objective



To demonstrate how to integrate with the PostHog API using Python for both sending (POST) and retrieving (GET) events.

This serves as a simple learning or portfolio project, using .env for safe configuration management and pandas for light analysis.



## Project Structure



````bash

├── posthog_post_event.py # Sends a test event to PostHog

├── posthog_get_events_pandas.py # Retrieves and filters events from PostHog

├── .env # (ignored) API keys and settings

├── .env.example # Example environment config

├── requirements.txt # Python dependencies

````



## Setup

1. Clone this repository
````bash
git clone https://github.com/lat35n-hrt/posthog_api.git
cd posthog_api_demo
````

2. Create a .env file
Use the provided .env.example and fill in your PostHog credentials:

```` bash
cp .env.example .env
````

3.   Install dependencies
(Use a virtual environment if preferred.)

````bash
pip install -r requirements.txt
````



##  Usage

- Send an Event

- Sends a test event (e.g., "manual_api_test") to PostHog.


```` bash
python posthog_post_event.py
````



You should receive a response like:



```` jspn
200
{"status":"ok"}
````


##  Retrieve Events

Fetches recent events and filters them using pandas.

```` bash
python posthog_get_events_pandas.py
````


Expected output (if events exist):



````cssharp
timestamp distinct_id event
0 2025-07-16T03:05:55.68Z user_001 manual_api_test
````


##  Notes

This project uses two different API keys:
- POSTHOG_API_KEY for sending events
- POSTHOG_PERSONAL_API_KEY for fetching data

All secrets are loaded from the .env file using python-dotenv.
Make sure to avoid pushing real API keys to GitHub.