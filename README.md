# PostHog Event Automation Tool

## 📌 Overview
This tool automates the following steps:
1. Fetch events from PostHog API
2. Save data as CSV
3. Generate a multilingual PDF report using fpdf2
4. Send the report via email

Built for demo and portfolio purposes.

## 🗂 Project Structure
```bash
├── run_all.py                  # Main orchestration script
├── posthog_get_events_pandas.py
├── generate_report.py
├── send_email.py
├── .env                        # Your environment config
├── .env.example                # Template for environment config
├── output/                     # CSV/PDF output (excluded from Git)
├── examples/                   # Standalone scripts (see README_example.md)

```

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
Use scripts in examples/ for unit-level testing:

````bash
cd examples/
python send_email_example.py
````

More details: examples/README_example.md

## 📎 Notes
.gitignore excludes output/, *.csv and *.pdf

Designed for learning, demo, and reproducible reporting

Easy to expand: plug-in style architecture