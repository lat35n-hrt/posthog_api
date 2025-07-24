# examples/generate_pdf_simple.py

from dotenv import load_dotenv
from fpdf import FPDF
import pandas as pd
import os

# === Load environment variables === #
load_dotenv()
PDF_PATH = os.getenv("PDF_PATH", "./output/report.pdf")
FONT_PATH = os.getenv("FONT_PATH", "./fonts/NotoSansJP-Regular.ttf")
FONT_NAME = os.getenv("FONT_NAME", "NotoSans")

# === Sample Data === #
# Hard coding for unit tests, including Japanese language
df = pd.DataFrame([
    {"timestamp": "2025-07-16T10:30:00", "distinct_id": "user_001", "event": "テストイベント"},
    {"timestamp": "2025-07-16T11:00:00", "distinct_id": "user_002", "event": "test_event"},
])

# === PDF Class === #
class PDF(FPDF):
    def header(self):
        self.set_font(FONT_NAME, size=14)
        self.cell(0, 10, text="PostHog Event Report", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(5)

    def add_table(self, df):
        self.set_font(FONT_NAME, size=10)
        col_width = self.epw / len(df.columns)

        for col in df.columns:
            self.cell(col_width, 10, col, border=1)
        self.ln()

        for _, row in df.iterrows():
            for item in row:
                self.cell(col_width, 10, str(item), border=1)
            self.ln()

# === Generate PDF === #
pdf = PDF()
if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"Font file not found: {FONT_PATH}")

pdf.add_font(FONT_NAME, fname=os.path.expanduser(FONT_PATH))
pdf.add_page()
pdf.add_table(df)

# === Save PDF === #
os.makedirs(os.path.dirname(PDF_PATH), exist_ok=True)
print(f"Saving to: {PDF_PATH}")
pdf.output(PDF_PATH)