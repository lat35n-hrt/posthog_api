import os
from dotenv import load_dotenv
from posthog_get_events_pandas import fetch_and_save_csv
from generate_report import generate_pdf_from_csv
from send_email import send_email
from datetime import datetime

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Script directory
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ENV
EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT", "Your PDF Report")
EMAIL_BODY = os.getenv("EMAIL_BODY", "Please find the attached PDF report.")
# csv_path = os.getenv("CSV_PATH", "./output/events.csv") # A default path is used for a unit test in send_enail.py only.
# pdf_path = os.getenv("PDF_PATH", "./output/report.pdf") # A default path is used for a unit test in send_enail.py only.
REL_FONT_PATH = os.getenv("FONT_PATH", "fonts/NotoSansJP-Regular.ttf")
FONT_PATH = os.path.join(BASE_DIR, REL_FONT_PATH)
FONT_NAME = os.getenv("FONT_NAME", "NotoSans")

# Date and Time
current_date_time = datetime.now().strftime("%Y%m%d_%H%M%S")

# Construct filenames with the date
# v2_blog enhancement: more specific filenames
csv_filename = f"blog_pageview_{current_date_time}.csv"
pdf_filename = f"blog_report_{current_date_time}.pdf"
CSV_PATH = os.path.join(OUTPUT_DIR, csv_filename)
PDF_PATH = os.path.join(OUTPUT_DIR, pdf_filename)

# 1. fetch data save csv
print("📡 Fetching data from PostHog API and saving to CSV...")
fetch_and_save_csv(CSV_PATH)

# 2. Generate PDF
print("📄 Reading CSV and generating PDF...")
generate_pdf_from_csv(CSV_PATH, PDF_PATH, FONT_PATH, FONT_NAME)

# 3. Send Email
print("📧 Sending email with PDF attached...")
send_email(EMAIL_SUBJECT, EMAIL_BODY, PDF_PATH)

print("✅ All steps completed successfully.")
