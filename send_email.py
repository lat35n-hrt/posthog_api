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
PDF_PATH = os.getenv("PDF_PATH", "./output/report.pdf")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT", "Your PDF Report")
EMAIL_BODY = os.getenv("EMAIL_BODY", "Please find the attached PDF report.")

def send_email(subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_ADDRESS
    msg.set_content(body)

    # Attach PDF file
    if PDF_PATH and os.path.exists(PDF_PATH):
        with open(PDF_PATH , "rb") as f:
            pdf_data = f.read()
            msg.add_attachment(
                pdf_data,
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(PDF_PATH),
            )
    else:
        print(f"⚠️ PDF file not found: {PDF_PATH}")
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
    send_email(EMAIL_SUBJECT, EMAIL_BODY, PDF_PATH)