# PostHog Event Automation Tool

## 📌 Overview
This tool automates the following steps:
1. Fetch events from PostHog API
2. Save data as CSV
3. Generate a multilingual PDF report using fpdf2
4. Send the report via email

Built for demo and portfolio purposes.


## ⚙️ Setup

1. Clone Repository
```bash
git clone https://github.com/lat35n-hrt/posthog_api.git
cd posthog_api
```

2. Install Dependencies

```bash
pip install -r requirements.txt
```

3. Configure .env
Use .env.example as a starting point:

```bash
cp .env.example .env
```

Set the following values:

API Keys: POSTHOG_API_KEY, POSTHOG_PERSONAL_API_KEY

Email Settings: EMAIL_ADDRESS, EMAIL_PASSWORD, TO_ADDRESS

Font & Output: FONT_PATH, PDF_PATH, etc.

⚠️ Font not included. Download NotoSansJP from Google Fonts

## 🚀 Run All Steps
```bash
python run_all.py
```

Expected steps:

✅ CSV created: ./output/events_yyyymmdd_hhmmss.csv

📄 PDF generated: ./output/report_yyyymmdd_hhmmss.pdf

📧 Email sent with PDF attached


## 🧪 For Standalone Feature Testing
Use scripts in sandbox/ for unit-level testing:

````bash
cd sandbox/
python send_email_example.py
````

More details: sandbox/README_example.md

## 📎 Notes
.gitignore excludes output/, *.csv and *.pdf

Designed for learning, demo, and reproducible reporting

Easy to expand: plug-in style architecture



## 📸 Screenshots
1. Triggering the PDF generation & email delivery

Below is the exact command execution that triggers the PostHog → PDF → Mail pipeline.

![Email Demo](img/cli_demo.png)


2. Delivered email with PDF attachment

The system successfully delivered the generated PDF to the test mailbox.

![Email Demo](img/sendmail_success.png)


## v1 Directory Split and Path Stability Notes

To prepare for the production-oriented implementation (v2), the project has been reorganized so that the
initial Proof-of-Concept (v1) is kept isolated under its own directory:

```bash
posthog_api/
├── v1_generic_events/ # PoC: basic PostHog → CSV → PDF → Email pipeline
├── v2_blog/ # Production-oriented blog integration (in progress)
└── ...
```

The goal of the v1 split is:

- to verify the minimal functional pipeline in a clean, controlled environment
- to prevent early v2 development from being affected by PoC-level experimental code
- to ensure the path behavior is stable when executed from different environments
  (local CLI, cron, CI, or future server-side execution)

# Developer notes

After moving run_all.py and related scripts into v1_generic_events/,
the original relative FONT_PATH (./fonts/...) no longer resolved correctly
when executing from the project root.

This fix ensures FONT_PATH is constructed as:

    BASE_DIR + REL_FONT_PATH

allowing both:
  - `cd v1_generic_events && python run_all.py`
  - `python v1_generic_events/run_all.py`

to work reliably without modifying existing .env values or directory structure.

This is a minimal and safe fix that restores original behavior.
