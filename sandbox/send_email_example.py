# send_email.py
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# .env
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_ADDRESS = os.getenv("TO_ADDRESS")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
PDF_PATH = os.getenv("PDF_PATH", "./output/report.pdf")
EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT", "Your PDF Report") # for unit test
EMAIL_BODY = os.getenv("EMAIL_BODY", "Please find the attached PDF report.") # for unit test

def send_email(subject: str, body: str, pdf_path: str = PDF_PATH):

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("❌ EMAIL_ADDRESS or EMAIL_PASSWORD is not set.")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_ADDRESS
    msg.set_content(body)

#    print("TO_ADDRESS =", TO_ADDRESS)

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


if __name__ == "__main__":
    send_email(EMAIL_SUBJECT, EMAIL_BODY)
