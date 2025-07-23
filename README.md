

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



## PDF Generation (Report Export)

You can generate a simple PDF report of the retrieved events using [fpdf2](https://github.com/PyFPDF/fpdf2).

### Prerequisites
Make sure the following environment variables are configured in your `.env` file:

CSV_INPUT_PATH=./data/sample_events.csv
PDF_FILENAME_BASE=fpdf_output
FONT_PATH=./fonts/NotoSansJP-Regular.ttf
FONT_NAME=NotoSans


These are also documented in `.env.example`.

### Run the Script

Use the script below to convert the CSV data to a formatted PDF:

```bash
python generate_report.py
```

Output
The generated PDF will be saved in the specified directory with a name like:


fpdf_output_20250719_232654.pdf

fpdf2 was chosen for its Unicode compatibility, especially for generating multilingual PDF reports.
In this project, we used NotoSansJP-Regular.ttf to verify Japanese language support.

Make sure the TTF font file (e.g. NotoSansJP-Regular.ttf) exists at the specified path.

⚠️ The font file is not included in the repository. You can download it from:
https://fonts.google.com/noto/specimen/Noto+Sans+JP


## 📧 Email PDF Report
This project includes a feature to send the generated PDF report as an email attachment.

### 🔧 Configuration

### Email Configuration
EMAIL_ADDRESS=your_email@gmail.com           # Sender address
EMAIL_PASSWORD=your_app_password             # App password (Gmail)
EMAIL_TO=recipient_email@example.com         # Recipient address
PDF_PATH=./output/fpdf_output.pdf            # Path to the PDF file
SMTP_SERVER=smtp.gmail.com                   # SMTP server (default for Gmail)
SMTP_PORT=465                                # Port for SSL (Gmail default)
EMAIL_SUBJECT=Your PDF Report
EMAIL_BODY=Please find the attached PDF report.
✅ Ensure that App Passwords are enabled if you're using Gmail with 2-step verification.

### 🚀 Send the Email
Run the following command to send the email:

````bash
python send_email.py
````

You should see a message like:

✅ Email sent successfully.