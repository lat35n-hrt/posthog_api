# 🧪 PostHog API Examples: Standalone Scripts

This directory contains simple standalone scripts to demonstrate key features of the PostHog API integration project:

- Send events via API
- Retrieve and filter events
- Generate a multilingual PDF report
- Send the report via email

Each script runs independently and uses mock data or `.env` settings.

---

## 📁 Directory Structure

```bash
examples/
├── posthog_post_event.py         # Send a test event
├── posthog_get_events_pandas.py # Retrieve and filter events
├── generate_pdf_simple.py       # Convert CSV data to PDF
├── send_email_example.py        # Send the generated PDF by email
├── .env.example                 # Sample environment settings
└── README_example.md            # (This file)
```

⚙️ Setup
1. Prepare .env
Copy the provided example and edit the necessary values:

````bash
cp .env.example .env
````

Typical settings include:

dotenv

# PostHog
POSTHOG_API_KEY=your_project_api_key
POSTHOG_PERSONAL_API_KEY=your_personal_api_key
POSTHOG_HOST=https://app.posthog.com

# Email
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
TO_ADDRESS=recipient@example.com

# PDF
FONT_PATH=./fonts/NotoSansJP-Regular.ttf
FONT_NAME=NotoSans
PDF_PATH=./output/fpdf_output.pdf
⚠️ Do not commit .env to GitHub.

▶️ 1. Send Event to PostHog
Sends a test event with mock distinct_id and action.

````bash
python posthog_post_event.py
````

Expected result:

````json
200
{"status":"ok"}
````

🔍 2. Get & Filter Events
Fetches event logs and filters them using pandas.

````bash
python posthog_get_events_pandas_example.py
````

Sample output:

````text
timestamp                  distinct_id   event
2025-07-16T11:00:00Z       user_002      test_event
````

🖨️ 3. Generate PDF Report
Creates a formatted PDF from mock event data (hardcoded or CSV).

````bash
python generate_report_example.py
````

Output file path is set in .env (e.g. ./output/fpdf_output.pdf).

✅ Uses fpdf2 and NotoSansJP-Regular.ttf for multilingual support (Japanese included).

✉️ 4. Send PDF by Email
Sends the generated PDF file as an attachment via Gmail SMTP.

````bash
python send_email_example.py
````

Make sure EMAIL_ADDRESS, EMAIL_PASSWORD, and TO_ADDRESS are configured in .env.

Expected message:

✅ Email sent successfully.


🔖 Notes
These are self-contained examples for quick testing and learning.

Use the main README.md for full project integration (run_all.py orchestration).

Font file (e.g. NotoSansJP) must be downloaded manually:
https://fonts.google.com/noto/specimen/Noto+Sans+JP

