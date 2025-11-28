# Installed fpdf2
from dotenv import load_dotenv
from fpdf import FPDF
import pandas as pd
import os
from datetime import datetime

# loading .env file
load_dotenv()

def generate_pdf_from_csv(csv_path: str, pdf_path: str, font_path: str, font_name: str):

    # Check files exist
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")

    # CSV input path
    df = pd.read_csv(csv_path)

    # PDF Class
    class PDF(FPDF):

        def __init__(self, font_path, font_name):
            super().__init__()
            self.add_font(font_name, fname=os.path.expanduser(font_path), uni=True)
            self.set_font(font_name, size=10)  # initial font

        def header(self):
            self.set_font("NotoSans", size=12)
            self.cell(0, 10, text="PostHog Blog Analytics Report", new_x="LMARGIN", new_y="NEXT", align="C")
            self.ln(5)

        def add_table(self, df):
            self.set_font("NotoSans", size=8) # Smaller font for readability

            # col_width = self.epw / len(df.columns)  # equal column width
            # Custom column widths (total should be ~190mm for A4)
            col_widths = {
                'timestamp': 32,      # 35 → 32
                'event': 20,          # 25 → 20
                'url': 55,            # 60 → 55
                'title': 35,          # 40 → 35
                'referrer': 35        # 40 → 35
            }


            # Define column order (exclude distinct_id)
            display_columns = ['timestamp', 'event', 'url', 'title', 'referrer']

            # Filter to only display columns that exist in the DataFrame
            columns = [col for col in display_columns if col in df.columns]

            # column
            for col in columns:
                self.cell(col_widths.get(col, 30), 10, col, border=1)
            self.ln()

            # row
            for _, row in df.iterrows():
                for col in columns:
                    width = col_widths.get(col, 30)
                    value = str(row[col])

                    # Format timestamp to be more readable
                    if col == 'timestamp' and 'T' in value:
                        # Convert "2025-11-27T11:21:22.930000+00:00" to "2025-11-27 11:21"
                        try:
                            dt = pd.to_datetime(value)
                            value = dt.strftime('%Y-%m-%d %H:%M')
                        except:
                            pass

                    # Replace 'nan' with '-'
                    if value.lower() == 'nan':
                        value = '-'

                    if len(str(value)) > 50:
                        value = str(value)[:47] + "..."

                    self.cell(width, 10, value, border=1)

                self.ln()


    pdf = PDF(font_path, font_name)
    pdf.add_page()
    pdf.add_table(df)


    print(f"Saving to: {pdf_path}")
    pdf.output(pdf_path)

