# Installed fpdf2
from dotenv import load_dotenv
from fpdf import FPDF
import pandas as pd
import os
from datetime import datetime

# loading .env file
load_dotenv()

# Get environment variables with defaults
csv_input_path = os.getenv("CSV_INPUT_PATH", "./data/sample_events.csv")  # default for clarity
font_path = os.getenv("FONT_PATH", "./fonts/NotoSansJP-Regular.ttf")
font_name = os.getenv("FONT_NAME", "NotoSans")
base_name = os.getenv("PDF_FILENAME_BASE", "fpdf_output")

# Check files exist
if not os.path.exists(csv_input_path):
    raise FileNotFoundError(f"CSV file not found: {csv_input_path}")
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font file not found: {font_path}")

# CSV input path
df = pd.read_csv(csv_input_path)

# PDF Class
class PDF(FPDF):
    def header(self):
        self.set_font("NotoSans", size=14)
        self.cell(0, 10, text="PostHog Event Report", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(5)

    def add_table(self, df):
        self.set_font("NotoSans", size=10)
        col_width = self.epw / len(df.columns)  # equal column width

        # column
        for col in df.columns:
            self.cell(col_width, 10, col, border=1)
        self.ln()

        # row
        for _, row in df.iterrows():
            for item in row:
                self.cell(col_width, 10, str(item), border=1)
            self.ln()

# Generate PDF
pdf = PDF()
pdf.add_font(font_name, fname=os.path.expanduser(font_path))
pdf.add_page()
pdf.add_table(df)

# File Output
date_suffix = datetime.now().strftime("_%Y%m%d_%H%M%S")
file_name = f"{base_name}{date_suffix}.pdf"
file_path = os.path.expanduser("~/Desktop/" + file_name)

print(f"Saving to: {file_path}")
pdf.output(file_path)