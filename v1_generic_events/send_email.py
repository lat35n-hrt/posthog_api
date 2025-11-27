# send_email.py
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Loading .env
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_ADDRESS = os.getenv("TO_ADDRESS")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT", "Your PDF Report") # for unit test
EMAIL_BODY = os.getenv("EMAIL_BODY", "Please find the attached PDF report.") # for unit test

if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, TO_ADDRESS]):
    raise EnvironmentError("Missing required environment variables for email sending.")

def send_email(subject: str, body: str, pdf_path: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_ADDRESS
    msg.set_content(body)

    # Attach PDF file
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path , "rb") as f:
            pdf_data = f.read()
            msg.add_attachment(
                pdf_data,
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(pdf_path),
            )
    else:
        print(f"⚠️ PDF file not found: {pdf_path}")
        return

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Unit Test
# Only send email when send_email.py is run directly, not when imported
if __name__ == "__main__":
    # When called from run_all.py, the path generated in run_all.py is applied
    test_pdf_path = os.getenv("PDF_PATH", "./output/report.pdf") # Test path
    send_email(EMAIL_SUBJECT, EMAIL_BODY, test_pdf_path) # test_pdf_path is uesd